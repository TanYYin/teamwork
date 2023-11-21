import keras
from keras.models import Model
import keras.backend as K
from keras.callbacks import Callback
from keras.optimizers import Adam
from keras.regularizers import l2
from bert4keras.models import build_transformer_model
from utils import seq_gather, extract_items, metric
from tqdm import tqdm
import numpy as np

# 关系SPO三元组 subject predicate object 计算公式 = h_N + v_sub_k
# 不是将关系视为实体对上的离散标签，而是将关系建模为将主体映射到对象的函数。
# 更准确地说，我们不是学习关系分类器 f(s,o) -> r，而是学习关系特定的标记器 f_{r}(s) -> o

bert_layers = 12

def E2EModel(bert_config_path, bert_checkpoint_path, LR, num_rels):

    bert_model = build_transformer_model(
            config_path=bert_config_path,
            checkpoint_path=bert_checkpoint_path,
            return_keras_model=True,
        ) # 搭建模型

    gold_sub_heads_in = keras.layers.Input(shape=(None,)) # 输入
    gold_sub_tails_in = keras.layers.Input(shape=(None,))
    sub_head_in = keras.layers.Input(shape=(1,))
    sub_tail_in = keras.layers.Input(shape=(1,))
    gold_obj_heads_in = keras.layers.Input(shape=(None, num_rels))
    gold_obj_tails_in = keras.layers.Input(shape=(None, num_rels))

    gold_sub_heads, gold_sub_tails, sub_head, sub_tail, gold_obj_heads, gold_obj_tails = gold_sub_heads_in, gold_sub_tails_in, sub_head_in, sub_tail_in, gold_obj_heads_in, gold_obj_tails_in
    tokens = bert_model.input[0]
    mask = keras.layers.Lambda(lambda x: K.cast(K.greater(K.expand_dims(x, 2), 0), 'float32'))(tokens) # 做mask 消除padding的影响

    output_layer = 'Transformer-2-FeedForward-Norm' # 三层bert模型
    tokens_feature = bert_model.get_layer(output_layer).output # h_N 也就是每个token的bert输出向量
    pred_sub_heads = keras.layers.Dense(1, activation='sigmoid')(tokens_feature) # 用于预测某个token是不是实体的开头部分
    pred_sub_tails = keras.layers.Dense(1, activation='sigmoid')(tokens_feature) # 用于预测某个token是不是实体的结尾部分

    subject_model = Model(bert_model.input, [pred_sub_heads, pred_sub_tails]) # 得到预测subject的模型


    sub_head_feature = keras.layers.Lambda(seq_gather)([tokens_feature, sub_head]) # subject开头的特征向量 1*len
    sub_tail_feature = keras.layers.Lambda(seq_gather)([tokens_feature, sub_tail]) # subject结尾的特征向量 1*len
    sub_feature = keras.layers.Average()([sub_head_feature, sub_tail_feature]) # subject的特征 取平均 1*len

    tokens_feature = keras.layers.Add()([tokens_feature, sub_feature]) # 得到所要的计算函数 h_N + v_sub_k
    pred_obj_heads = keras.layers.Dense(num_rels, activation='sigmoid')(tokens_feature) # 有多少种关系 就有多少层 预测subject在某种关系下对应object的开头
    pred_obj_tails = keras.layers.Dense(num_rels, activation='sigmoid')(tokens_feature) # 预测subject在某种关系下对应object的开头

    # 得到预测subject在某种关系下对应object的模型
    object_model = Model(bert_model.input + [sub_head_in, sub_tail_in], [pred_obj_heads, pred_obj_tails]) 


    hbt_model = Model(bert_model.input + [gold_sub_heads_in, gold_sub_tails_in, sub_head_in, sub_tail_in, gold_obj_heads_in, gold_obj_tails_in],
                        [pred_sub_heads, pred_sub_tails, pred_obj_heads, pred_obj_tails]) # 也就是联合训练的模型

    gold_sub_heads = K.expand_dims(gold_sub_heads, 2)
    # 训练标签 因为在处理数据的输入的时候 会把输入数据处理成层叠式指针标注框架所需要的格式 所以输入标签要进行扩维
    gold_sub_tails = K.expand_dims(gold_sub_tails, 2)

    sub_heads_loss = K.binary_crossentropy(gold_sub_heads, pred_sub_heads) # 计算损失 二分类交叉熵损失
    sub_heads_loss = K.sum(sub_heads_loss * mask) / K.sum(mask) # 计算损失时不受padding字符的影响
    sub_tails_loss = K.binary_crossentropy(gold_sub_tails, pred_sub_tails)
    sub_tails_loss = K.sum(sub_tails_loss * mask) / K.sum(mask)

    obj_heads_loss = K.sum(K.binary_crossentropy(gold_obj_heads, pred_obj_heads), 2, keepdims=True)
    obj_heads_loss = K.sum(obj_heads_loss * mask) / K.sum(mask)
    obj_tails_loss = K.sum(K.binary_crossentropy(gold_obj_tails, pred_obj_tails), 2, keepdims=True)
    obj_tails_loss = K.sum(obj_tails_loss * mask) / K.sum(mask)

    loss = (sub_heads_loss + sub_tails_loss) + (obj_heads_loss + obj_tails_loss) # 把所有loss加起来

    hbt_model.add_loss(loss) # 将loss添加到模型里面
    hbt_model.compile(optimizer=Adam(LR)) # 模型编译
    hbt_model.summary()

    return subject_model, object_model, hbt_model

class Evaluate(Callback):

    def __init__(self, subject_model, object_model, tokenizer, id2rel, eval_data, save_weights_path, min_delta=1e-4, patience=7):
        self.patience = patience
        self.min_delta = min_delta
        self.monitor_op = np.greater
        self.subject_model = subject_model
        self.object_model = object_model
        self.tokenizer = tokenizer
        self.id2rel = id2rel
        self.eval_data = eval_data
        self.save_weights_path = save_weights_path

    def on_train_begin(self, logs=None):

        self.step = 0
        self.wait = 0
        self.stopped_epoch = 0
        self.warmup_epochs = 2
        self.best = -np.Inf

    # 由于模型所用数据不一般 所以需要自己设计一个计算精确度 召回率 f1值的函数
    def on_epoch_end(self, epoch, logs=None):

        precision, recall, f1 = metric(self.subject_model, self.object_model, self.eval_data, self.id2rel, self.tokenizer)
        if self.monitor_op(f1 - self.min_delta, self.best) or self.monitor_op(self.min_delta, f1):
            self.best = f1
            self.wait = 0
            self.model.save_weights(self.save_weights_path) # 模型如果达到最优就进行保存
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True
        print('f1: %.4f, precision: %.4f, recall: %.4f, best f1: %.4f\n' % (f1, precision, recall, self.best))

    # 提前结束训练函数
    def on_train_end(self, logs=None):

        if self.stopped_epoch > 0:
            print('Epoch %05d: early stopping' % (self.stopped_epoch + 1))
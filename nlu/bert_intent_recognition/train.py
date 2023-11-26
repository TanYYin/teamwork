import json
import pandas as pd 
import numpy as np 

from bert4keras.backend import keras
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding, DataGenerator
from sklearn.metrics import classification_report
from bert4keras.optimizers import Adam

from bert_model import build_bert_model
from data_helper import load_data

#定义超参数和配置文件
class_nums = 13
maxlen = 128
batch_size = 8

config_path='./chinese_rbt3_L-3_H-768_A-12/bert_config_rbt3.json'
checkpoint_path='./chinese_rbt3_L-3_H-768_A-12/bert_model.ckpt'
dict_path = './chinese_rbt3_L-3_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path)

class data_generator(DataGenerator):

    def __iter__(self, random=False):

        batch_token_ids, batch_segment_ids, batch_labels = [], [], [] # token的序列列表 分隔符的序列列表 labels的序列列表
        for is_end, (text, label) in self.sample(random):
            token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen) # 用上面词库的生成器对原句进行编码
            batch_token_ids.append(token_ids)
            batch_segment_ids.append(segment_ids)
            batch_labels.append([label])
            if len(batch_token_ids) == self.batch_size or is_end:
                batch_token_ids = sequence_padding(batch_token_ids) # 最大长度padding或截断
                batch_segment_ids = sequence_padding(batch_segment_ids)
                batch_labels = sequence_padding(batch_labels)
                yield [batch_token_ids, batch_segment_ids], batch_labels # 模型的输入
                batch_token_ids, batch_segment_ids, batch_labels = [], [], []

if __name__ == '__main__':

    # 加载数据集
    train_data = load_data('train.csv')
    test_data = load_data('test.csv')

    # 转换数据集
    train_generator = data_generator(train_data, batch_size)
    test_generator = data_generator(test_data, batch_size)

    model = build_bert_model(config_path,checkpoint_path,class_nums)
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=Adam(5e-6), 
        metrics=['accuracy'],
    )

    earlystop = keras.callbacks.EarlyStopping(
        monitor='val_loss', 
        patience=2, 
        verbose=2, 
        mode='min'
        )
    bast_model_filepath = 'best_model.weights'
    checkpoint = keras.callbacks.ModelCheckpoint(
        bast_model_filepath, 
        monitor='val_loss', 
        verbose=1, 
        save_best_only=True,
        mode='min'
        )

    model.fit_generator(
        train_generator.forfit(),
        steps_per_epoch=len(train_generator),
        epochs=10,
        validation_data=test_generator.forfit(), 
        validation_steps=len(test_generator),
        shuffle=True, 
        callbacks=[earlystop,checkpoint]
    )

    model.load_weights('best_model.weights')
    test_pred = []
    test_true = []
    for x,y in test_generator:
        p = model.predict(x).argmax(axis=1)
        test_pred.extend(p)

    test_true = test_data[:,1].tolist()
    print(set(test_true))
    print(set(test_pred))

    target_names = [line.strip() for line in open('label','r',encoding='utf8')]
    print(classification_report(test_true, test_pred,target_names=target_names))
import keras
import keras.backend as K
from keras.models import Model

class ESIM(object):

    def __init__( self, params):

        self._params = params

    def make_embedding_layer(self,name='embedding',embed_type='char',**kwargs):

        def init_embedding(weights=None):

            if embed_type == "char": # 如果是字符级
                input_dim = self._params['max_features'] # 输入的维度
                output_dim = self._params['embed_size'] # 输出的维度
            else:
                input_dim = self._params['word_max_features']
                output_dim = self._params['word_embed_size']

            return keras.layers.Embedding( # 调用embedding层
                input_dim = input_dim,
                output_dim = output_dim,
                trainable = False,
                name = name,
                weights = weights,
                **kwargs)

        if embed_type == "char": # 如果是字符级
            embed_weights = self._params['embedding_matrix'] # 权重是字符级词嵌入权重矩阵
        else:
            embed_weights = self._params['word_embedding_matrix'] # 权重是单词级词嵌入权重矩阵

        if embed_weights == []: # 如果权重矩阵是空
            embedding = init_embedding() # 直接调用embedding层
        else:
            embedding = init_embedding(weights = [embed_weights]) # 给embedding层传入权重矩阵

        return embedding

    def _make_multi_layer_perceptron_layer(self) -> keras.layers.Layer:

        # TODO: do not create new layers for a second call
        def _wrapper(x):
            activation = self._params['mlp_activation_func'] # 指定多层感知机的激活函数
            for _ in range(self._params['mlp_num_layers']): # 设定要构建几层全连接层
                x = keras.layers.Dense(self._params['mlp_num_units'],
                                       activation=activation)(x) # 构建n-1层输出是神经元属全连接层
            return keras.layers.Dense(self._params['mlp_num_fan_out'],
                                      activation=activation)(x) # 最后一层输出是设定的多层感知机的输出维度

        return _wrapper

    def _make_inputs(self) -> list:

        input_left = keras.layers.Input(
            name='text_left',
            shape=self._params['input_shapes'][0]
        )
        input_right = keras.layers.Input(
            name='text_right',
            shape=self._params['input_shapes'][1]
        )
        return [input_left, input_right] # 定义输入层

    def _make_output_layer(self) -> keras.layers.Layer: # 定义输出层

        task = self._params['task'] # 获取想做的选择
        if task == "Classification": # 如果是想分类
            return keras.layers.Dense(self._params['num_classes'], activation='softmax') # 使用softmax进行多(2)分类
        elif task == "Ranking": # 如果是想排序
            return keras.layers.Dense(1, activation='linear') # 输出
        else:
            raise ValueError(f"{task} is not a valid task type."
                             f"Must be in `Ranking` and `Classification`.")

    def build(self):

        a, b = self._make_inputs() # 模型是多输入的

        # ---------- Embedding layer ---------- #
        embedding = self.make_embedding_layer() # 定义一个词向量层作为两个输入的共享embedding
        embedded_a = embedding(a)
        embedded_b = embedding(b)

        # ---------- Encoding layer ---------- #
        # encoded_a = keras.layers.Bidirectional(keras.layers.LSTM(
        #     self._params['lstm_units'],
        #     return_sequences=True,
        #     dropout=self._params['dropout_rate']
        # ))(embedded_a)
        # encoded_b = keras.layers.Bidirectional(keras.layers.LSTM(
        #     self._params['lstm_units'],
        #     return_sequences=True,
        #     dropout=self._params['dropout_rate']
        # ))(embedded_b)

        bilstm = keras.layers.Bidirectional(keras.layers.LSTM( # 共享参数的bilstm结构 提取query和doc的语义向量
                    self._params['lstm_units'],
                    return_sequences=True,
                    dropout=self._params['dropout_rate']
                ))

        encoded_a = bilstm(embedded_a) # 把隐藏状态的值保留下来
        encoded_b = bilstm(embedded_b)

        # ---------- Local inference layer ---------- # 本地推理层
        atten_a, atten_b = SoftAttention()([encoded_a, encoded_b]) # 词向量相乘 如果两个词相似乘积较大 softmax求出权重
        # atten_a = 权重 * encoded_b
        # atten_b = 权重 * encoded_a

        sub_a_atten = keras.layers.Lambda(lambda x: x[0]-x[1])([encoded_a, atten_a])
        sub_b_atten = keras.layers.Lambda(lambda x: x[0]-x[1])([encoded_b, atten_b])

        mul_a_atten = keras.layers.Lambda(lambda x: x[0]*x[1])([encoded_a, atten_a])
        mul_b_atten = keras.layers.Lambda(lambda x: x[0]*x[1])([encoded_b, atten_b])

        # ESIM主要是计算新旧序列之间的差和积 并把所有信息合并起来储存在一个序列中？
        m_a = keras.layers.concatenate([encoded_a, atten_a, sub_a_atten, mul_a_atten])
        m_b = keras.layers.concatenate([encoded_b, atten_b, sub_b_atten, mul_b_atten])

        # ---------- Inference composition layer ---------- # 推理成分层
        # ESIM最后还需要综合所有信息 做一个全局的分析 这个过程依然是通过BiLSTM处理这两个序列
        composition_a = keras.layers.Bidirectional(keras.layers.LSTM(
            self._params['lstm_units'],
            return_sequences=True,
            dropout=self._params['dropout_rate']
        ))(m_a)

        # 因为考虑到求和运算对于序列长度是敏感的 因而降低了模型的鲁棒性 所以ESIM选择同时对两个序列进行average pooling和max pooling
        avg_pool_a = keras.layers.GlobalAveragePooling1D()(composition_a)
        max_pool_a = keras.layers.GlobalMaxPooling1D()(composition_a)

        composition_b = keras.layers.Bidirectional(keras.layers.LSTM(
            self._params['lstm_units'],
            return_sequences=True,
            dropout=self._params['dropout_rate']
        ))(m_b)

        avg_pool_b = keras.layers.GlobalAveragePooling1D()(composition_b)
        max_pool_b = keras.layers.GlobalMaxPooling1D()(composition_b)

        print(K.int_shape(composition_b))
        print(K.int_shape(avg_pool_b))

        pooled = keras.layers.concatenate([avg_pool_a, max_pool_a, avg_pool_b, max_pool_b])
        pooled = keras.layers.Dropout(rate=self._params['dropout_rate'])(pooled)

        # ---------- Classification layer ---------- # 分类层
        mlp = self._make_multi_layer_perceptron_layer()(pooled) # 送入多层感知机
        mlp = keras.layers.Dropout(
            rate=self._params['dropout_rate'])(mlp)

        prediction = self._make_output_layer()(mlp) # 输出层使用softmax进行分类

        model = Model(inputs=[a, b], outputs=prediction)

        return model
        
class SoftAttention(object):

    def __call__(self, inputs):

        a = inputs[0]
        b = inputs[1]

        attention = keras.layers.Lambda(self._attention,
                                        output_shape = self._attention_output_shape,
                                        arguments = None)(inputs)

        align_a = keras.layers.Lambda(self._soft_alignment,
                                     output_shape = self._soft_alignment_output_shape,
                                     arguments = None)([attention, b])
        align_b = keras.layers.Lambda(self._soft_alignment,
                                     output_shape = self._soft_alignment_output_shape,
                                     arguments = None)([attention, a])

        return align_a, align_b

    def _attention(self, inputs):

        attn_weights = K.batch_dot(x=inputs[0],
                                   y=K.permute_dimensions(inputs[1],
                                                          pattern=(0, 2, 1)))
        return K.permute_dimensions(attn_weights, (0, 2, 1))

    def _attention_output_shape(self, inputs):

        input_shape = inputs[0]
        embedding_size = input_shape[1]
        return (input_shape[0], embedding_size, embedding_size)

    def _soft_alignment(self, inputs):

        attention = inputs[0]
        sentence = inputs[1]

        # Subtract the max. from the attention weights to avoid overflows.
        exp = K.exp(attention - K.max(attention, axis=-1, keepdims=True))
        exp_sum = K.sum(exp, axis=-1, keepdims=True)
        softmax = exp / exp_sum

        return K.batch_dot(softmax, sentence)

    def _soft_alignment_output_shape(self, inputs):

        attention_shape = inputs[0]
        sentence_shape = inputs[1]
        return (attention_shape[0], attention_shape[1], sentence_shape[2])
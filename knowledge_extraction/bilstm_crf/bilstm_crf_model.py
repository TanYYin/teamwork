import keras
from crf_layer import CRF

class BiLstmCrfModel(object):

    def __init__(
            self, 
            max_len, # 句子最大长度
            vocab_size, # 词向量字典的大小
            embedding_dim, # 词向量的维度
            lstm_units, # lstm隐层单元的数量
            class_nums, # 标签类型的数量
            embedding_matrix=None # 词向量矩阵
            ):
        super(BiLstmCrfModel, self).__init__()
        self.max_len = max_len
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.lstm_units = lstm_units
        self.class_nums = class_nums
        self.embedding_matrix = embedding_matrix
        if self.embedding_matrix is not None:
            self.vocab_size,self.embedding_dim = self.embedding_matrix.shape

    def build(self): # 建立模型

        inputs = keras.layers.Input(
                shape=(self.max_len,), # 限定了句子矩阵的最大长度
                dtype='int32'
            )
        x = keras.layers.Masking(
                mask_value=0 # 如果句子长度不够 则会用0补充
            )(inputs)
        x = keras.layers.Embedding(
                input_dim=self.vocab_size, # 输入是词向量表的大小
                output_dim=self.embedding_dim, # 输出是词向量的维度
                trainable=False, # （不）做训练
                weights=self.embedding_matrix,
                mask_zero=True
            )(x)
        x = keras.layers.Bidirectional( # 接双向LSTM层
                keras.layers.LSTM(
                    self.lstm_units, 
                    return_sequences=True # 返回序列 输出每个字的特征
                )
            )(x)
        x = keras.layers.TimeDistributed(
                keras.layers.Dropout(
                    0.2
                )
            )(x)
        crf = CRF(self.class_nums) # 标签数量有多少种
        outputs = crf(x) # 输出
        model = keras.Model(inputs=inputs, outputs=outputs)
        model.compile(
            optimizer='adam', # 优化器
            loss=crf.loss_function, # 损失函数
            metrics=[crf.accuracy] # 每个字符的准确率
            )
        print(model.summary())

        return model
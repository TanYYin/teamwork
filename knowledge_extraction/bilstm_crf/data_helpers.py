import re,os
from itertools import chain
from collections import Counter
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
import numpy as np

class NerDataProcessor(object):

    def __init__(self,max_len,vocab_size):

        super(NerDataProcessor, self).__init__()
        self.max_len = max_len # 句子最大长度
        self.vocab_size = vocab_size # 词向量字典的大小
        self.word2id = {} # 词转ID

        self.tags = [] # 标签集
        self.tag2id = {} # 标签转ID
        self.id2tag = {} # ID转标签
        
        self.class_nums = 0 # 标签种类的数量
        self.sample_nums = 0 # 句子样本的数量

    def read_data(self,path,is_training_data=True): # 如果是训练测试集

        X = []
        y = []
        sentence = []
        labels = []
        split_pattern = re.compile(r'[；;。，、？！\.\?,! ]') # 切分句子
        with open(path,'r',encoding = 'utf8') as f:
            for line in f.readlines():
                # 每行为一个字符和其tag，中间用tab或者空格隔开
                line = line.strip().split()
                if(not line or len(line) < 2): # 如果是空行或者字符小于2 当成这个句子结束了 执行和正常句子结束一样的步骤
                    X.append(sentence.copy()) # 将整个句子加进去列表 因为此时没有word和tag可以继续放进去句子了
                    y.append(labels.copy())
                    sentence.clear() # 清空句子
                    labels.clear()
                    continue
                word, tag = line[0], line[1] # 如果是正常的 “词 标签” 格式
                tag = tag if tag != 'o' else 'O'
                if split_pattern.match(word) and len(sentence) >= self.max_len: # 如果此时已经达到了句子最大长度
                    sentence.append(word) # 最后这个词加进去句子
                    labels.append(tag)
                    X.append(sentence.copy()) # 将整个句子加进去列表
                    y.append(labels.copy())
                    sentence.clear() # 清空句子
                    labels.clear()
                else: # 如果还没达到句子最大长度
                    sentence.append(word) # 将当前的词加进去句子
                    labels.append(tag)
            if len(sentence): # 如果没有下一个词了 也就是 读到最后一个句子了
                X.append(sentence.copy()) # 将整个句子加进去列表
                sentence.clear() # 清空句子
                y.append(labels.copy())
                labels.clear()

        if is_training_data: # 如果是训练数据 就需要计算下面这些列表和字典
            self.tags = sorted(list(set(chain(*y)))) # 得到所有标签
            self.tag2id = {tag : idx + 1 for idx,tag in enumerate(self.tags)} # 标签转id
            self.id2tag = {idx + 1 : tag for idx,tag in enumerate(self.tags)} # id转标签
            # 将 x 进行padding的同时也需要对标签进行相应的padding
            self.tag2id['padding'] = 0 # 填充
            self.id2tag[0] = 'padding' # 填充
            self.class_nums = len(self.id2tag) # 标签种类的数量
            self.sample_nums = len(X) # 句子样本的数量

            vocab = list(chain(*X)) # 得到所有字
            print("vocab lenth",len(set(vocab))) # 不同字的数量
            print(self.id2tag) # 输出id转标签的字典
            vocab = Counter(vocab).most_common(self.vocab_size-2) # 用出现最多到倒数第三的字生成列表 字 出现次数
            vocab = [v[0] for v in vocab] # 得到出现最多到倒数第三的字
            for index,word in enumerate(vocab):
                self.word2id[word] = index + 2 # 词转id

            # OOV 为1，padding为0
            self.word2id['padding'] = 0
            self.word2id['OOV'] = 1

        return X,y

    def encode(self,X,y):

        X = [[self.word2id.get(word,1) for word in x] for x in X ] # 将字映射成字id
        X = pad_sequences(X,maxlen=self.max_len,value=0) # 填充和截断
        y = [[self.tag2id.get(tag,0) for tag in t] for t in y ] # 将标签映射成标签id
        y = pad_sequences(y,maxlen=self.max_len,value=0) # 填充和截断

        def label_to_one_hot(index: []): # 转成每个词都写成关于标签的独热码00001000这样

            data = []
            for line in index:
                data_line = []
                for i, index in enumerate(line):
                    line_line = [0]*self.class_nums # 每个词起始都是00000000
                    line_line[index] = 1 # 在标签转id的下标地方改为1 得到00001000
                    data_line.append(line_line) # 集合句子中的每一个词
                data.append(data_line) # 集合每一个句子
            return np.array(data)

        y = label_to_one_hot(index=y)
        print(y.shape)

        return X,y
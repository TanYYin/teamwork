import pickle
import pandas as pd

from esim import ESIM
from train import esim_params
from data_helper import pad_sequences
from bm25_retrival import BM25Retrieval

# 排序用的是拆成n个二分类任务 先使用bm25算法从词库召回初步最相似的20个召回词
# 然后使用esim模型计算原词与每个召回词的相似度 这个时候如果最相似的召回词与规范词不一样 就当作负样本输出
# 负样本可以再加入训练集上
class EntityMatch(object):

    def __init__(self,kb_path):

        super(EntityMatch, self).__init__()
        self.kb_path = kb_path
        self.bm25re = BM25Retrieval(self.kb_path) # 指定召回函数

        self.word2idx, _ = pickle.load(open("./checkpoint/word2id.pkl","rb")) # 拿到字转id的字典
        self.model = ESIM(esim_params).build() # 构建模型
        self.model.load_weights('./checkpoint_test/best_esim_model.h5') # 加载权重

    def char_index(self, p_sentences, h_sentences):

        p_list, h_list = [], []
        for p_sentence, h_sentence in zip(p_sentences, h_sentences):
            # 原词和规范词都转成 字1id 字2id 字3id 的形式
            p = [self.word2idx[word.lower()] for word in p_sentence if len(word.strip()) > 0 and word.lower() in self.word2idx.keys()]
            h = [self.word2idx[word.lower()] for word in h_sentence if len(word.strip()) > 0 and word.lower() in self.word2idx.keys()]

            p_list.append(p) # 得到原词id形式
            h_list.append(h) # 得到规范词id形式

        p_list = pad_sequences(p_list, maxlen=esim_params['input_shapes'][0][0]) # 得到填充后的 nb_samples * maxlen 矩阵
        h_list = pad_sequences(h_list, maxlen=esim_params['input_shapes'][0][0])

        return p_list, h_list # 返回两个填充后的矩阵

    def predict(self,query):

        cand_docs = self.bm25re.retrieval(query,20) # 召回最接近的前20个
        querys = [query] * len(cand_docs) # 复制20次 使原词和从知识库里召回的词一样多个

        p,h = self.char_index(querys,cand_docs) # 一个原词对一个召回的词

        scores = self.model.predict([p,h]) # 使用esim模型计算原词与每个召回词的接近程度
        scores = scores[:,1] # 拿到全部接近程度
        match_score = {e:s for e,s in zip(cand_docs,scores)} # 每一个召回词对应一个接近程度
        match_score = sorted(match_score.items(),key=lambda x:x[1],reverse=True) # 排序
        return match_score[0],cand_docs # 返回最高接近程度的词与其相似度 20个召回词

if __name__ == '__main__':

    emm = EntityMatch("./yidu-n7k/code.txt") # 为bm25+esim模型指定知识库
    test = pd.read_csv("./data/test.csv") # 指定测试集
    total = len(test) # 要测试的原词个数
    correct = 0 # 用于记录预测正确个数
    for raw,norm in test[["sentence1","sentence2"]].values: # 拿到原词和规范词
        pred,cand_docs = emm.predict(raw) # 拿到最高接近程度的词与其相似度 20个召回词
        if norm == pred[0]: # 如果接近程度最高的召回词和规范词一样
            correct += 1
        if pred[1] > 0.8 and norm != pred[0]: # 如果不一样且接近程度大于0.8
            print(raw,norm,"可以做负样本")

    print("\n","acc:",correct/total) # 输出测试结果
from gensim.summarization import bm25

class BM25Retrieval(object):

    def __init__(self, path): # 传进来就是知识库的路径

        super(BM25Retrieval, self).__init__()
        self.path = path
        self.kb_entitys = self.load_corpus(self.path) # 拿到知识库的全部实体列表
        self.bm25Model = bm25.BM25([list(i) for i in self.kb_entitys]) # 把实体名称都拆分成字符级别 得到二维列表

    def load_corpus(self,path):

        kb_entitys = [] # 建立一个空列表 用于存放实体
        with open(path,encoding='utf8') as f:
            for line in f.readlines(): # 知识库每行有两个数据 编码 实体名称
                code,name = line.strip().split('\t') # 分开编码和实体名称
                kb_entitys.append(name) # 实体都存进去列表

        return kb_entitys # 返回全部实体列表

    def retrieval(self,query,top_k):

        scores = self.bm25Model.get_scores(query) # 计算每个原词对知识库里的实体的接近程度
        match_score = {e:s for e,s in zip(self.kb_entitys,scores)} # 每一个实体对应一个接近程度
        match_score = sorted(match_score.items(),key=lambda x:x[1],reverse=True) # 按接近程度排序
        return [i[0] for i in match_score[:top_k]] # 返回前top_k个
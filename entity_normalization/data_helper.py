import os
import pickle
import numpy as np
import pandas as pd
from bm25_retrival import BM25Retrieval

total = 0
error = 0
def gen_training_data(raw_data_dir): # 传入原始数据所在的文件夹

    train_df = pd.read_excel(os.path.join(raw_data_dir,"train.xlsx")) # 读入原始训练数据
    answer_df = pd.read_excel(os.path.join(raw_data_dir,"answer.xlsx"))
    val_df = pd.read_excel(os.path.join(raw_data_dir,"val.xlsx"))

    bm25Model = BM25Retrieval(os.path.join(raw_data_dir,"code.txt")) # bm25做召回模型 code.txt是知识库

    # 原报错UnboundLocalError: local variable 'total' referenced before assignment
    # 原为
    # total = 0
    # error = 0

    def gen_negtive_sample(raw,norm): # 生成负样本 原词 规范词

        cand_entity = bm25Model.retrieval(raw,10) # 根据原词召回10个词
        global total
        total += 1
        try:
            cand_entity.remove(norm) # 如果召回的里面10个词里面含有规范词 就去掉其中的规范词
        except:
            global error
            error += 1
        return cand_entity # 返回不含规范词的召回列表 即负样本

    def match_positive_sample(list1,list2): # 找正样本 将原本1对多 多对1 多对多 变成1对1

        ress = []
        for e1 in list1:
            score = 0
            pos_e = ""
            for e2 in list2:
                s = len(set(e1)&set(e2))
                if s > score:
                    score = s
                    pos_e = e2
            if pos_e != "":
                ress.append([e1,pos_e])

        return ress

    train = [] # 建立一个空列表用于存放训练集
    data = np.concatenate([train_df.values , answer_df.values],axis=0)
    for raw_entity,norm_entity in data:
        # 因为原词是XXX+YYY+ZZZ 规范词是AAA##BBB##CCC 所以需要切割开多个实体
        if '+' not in raw_entity and "##" not in norm_entity: # 如果有1个原词和1个规范词
            train.append([raw_entity,norm_entity,1]) # 正样本是1
            for neg in gen_negtive_sample(raw_entity,norm_entity): # 生成负样本
                train.append([raw_entity,neg,0]) # 负样本是0
        elif '+' not in raw_entity and "##" in norm_entity: # 如果有1个原词和n个规范词
            for ne in norm_entity.split("##"): # 切割出每一个规范词
                train.append([raw_entity,ne,1])
                for neg in gen_negtive_sample(raw_entity,ne):
                    train.append([raw_entity,neg,0])
        elif '+' in raw_entity and "##" in norm_entity: # 如果有n个原词和n个规范词
            ne_list = norm_entity.split("##") # 切割出每一个规范词
            re_list = raw_entity.split("+") # 切割出每一个原词
            for raw_ent,norm_ent in match_positive_sample(re_list,ne_list):
                train.append([raw_ent,norm_ent,1])
                for neg in gen_negtive_sample(raw_ent,norm_ent):
                    train.append([raw_ent,neg,0])
        else: # 如果有n个原词和1个规范词
            re_list = raw_entity.split("+") # 切割出每一个原词
            for re in re_list:
                train.append([re,norm_entity,1])
                for neg in gen_negtive_sample(re,norm_entity):
                    train.append([re,neg,0])

    train = pd.DataFrame(train) # 训练集由列表转格式
    train.columns = ["sentence1","sentence2","label"] # 设定抬头
    train.drop_duplicates(subset=["sentence1","sentence2"],keep='first') # 去重

    test = [] # 建立一个空列表用于存放测试集 不生成负样本 只生成正样本
    for raw_entity,norm_entity in val_df.values:
        # 因为原词是XXX+YYY+ZZZ 规范词是AAA##BBB##CCC 所以需要切割开多个实体
        if '+' not in raw_entity and "##" not in norm_entity: # 如果有1个原词和1个规范词
            test.append([raw_entity,norm_entity,1])

        elif '+' not in raw_entity and "##" in norm_entity: # 如果有1个原词和n个规范词
            for ne in norm_entity.split("##"): # 切割出每一个规范词
                test.append([raw_entity,ne,1])

        elif '+' in raw_entity and "##" in norm_entity: # 如果有n个原词和n个规范词
            ne_list = norm_entity.split("##") # 切割出每一个规范词
            re_list = raw_entity.split("+") # 切割出每一个原词
            for raw_ent,norm_ent in match_positive_sample(re_list,ne_list):
                test.append([raw_ent,norm_ent,1])
        else: # 如果有n个原词和1个规范词
            re_list = raw_entity.split("+") # 切割出每一个原词
            for re in re_list:
                test.append([re,norm_entity,1])

    test = pd.DataFrame(test) # 测试集由列表转格式
    test.columns = ["sentence1","sentence2","label"] # 设定抬头

    train.to_csv("./data/train.csv",index=False,encoding="utf8") # 保存
    test.to_csv("./data/test.csv",index=False,encoding="utf8")
    print(train.shape) # 输出训练集的大小
    print("bm25 未召回正确规范实体的比例：",error / total) # 输出未召回正确规范实体的比例

    return train,test

def pad_sequences(sequences, maxlen=None, dtype='int32', padding='post', truncating='post', value=0.):

    lengths = [len(s) for s in sequences] # 所有词的长度列表

    nb_samples = len(sequences) # 有多少个词
    if maxlen is None: # 如果没指定最大长度
        maxlen = np.max(lengths) # 就以最长词的长度为最大长度

    x = (np.ones((nb_samples, maxlen)) * value).astype(dtype) # 建立一个全为指定填充数字的矩阵 shape为 nb_samples * maxlen
    for idx, s in enumerate(sequences):
        if len(s) == 0:
            continue  # 发现空列表
        if truncating == 'pre': # 如果想在前面填充
            trunc = s[-maxlen:]
        elif truncating == 'post': # 如果想在后面填充
            trunc = s[:maxlen]
        else:
            raise ValueError("Truncating type '%s' not understood" % padding) # 不能理解目前的填充方式

        if padding == 'post':
            x[idx, :len(trunc)] = trunc # 在后面填充 就是 把前面maxlen的填充数字改为词
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc # 在前面填充 就是 把后面maxlen的填充数字改为词
        else:
            raise ValueError("Padding type '%s' not understood" % padding) # 不能根据目前的填充方式进行填充
    return x # 返回填充后的 nb_samples * maxlen 矩阵


def shuffle(*arrs):

    arrs = list(arrs)
    for i, arr in enumerate(arrs):
        assert len(arrs[0]) == len(arrs[i])
        arrs[i] = np.array(arr)
    p = np.random.permutation(len(arrs[0]))
    return tuple(arr[p] for arr in arrs)

def load_char_vocab():

    if os.path.exists("./checkpoint/word2id.pkl"): # 字转id的字典是否存在
        word2idx, idx2word = pickle.load(open("./checkpoint/word2id.pkl","rb")) # 存在的话就直接加载
    else: # 如果字典不存在
        df = pd.read_csv("./data/train.csv",encoding="utf8") # 打开训练集数据
        vocab = [] # 建一个空列表用于存放字
        for ent in df["sentence1"].tolist()+df["sentence2"].tolist(): # 拿到 原词 和 规范词
            # 原报错TypeError: 'float' object is not iterable
            # 原为
            # vocab.extend(list(ent))
            try:
                vocab.extend(list(ent)) # 原词和规范词的字都存进去列表
            except:
                continue

        with open(os.path.join("./yidu-n7k/code.txt"),encoding='utf8') as f: # 拿到知识库
            for line in f.readlines(): # 知识库每行有两个数据 编码 实体名称
                code,name = line.strip().split('\t') # 分开编码和实体名称
                vocab.extend(list(name)) # 实体的字都存进去列表

        vocab = sorted(set(vocab)) # 去重并排序
        print(len(vocab)) # 输出一共有多少个不同字
        word2idx = {word: index for index, word in enumerate(vocab,start=2)} # 建立一个字到id的字典
        word2idx["UNK"] = 1 # 其中UNK的id为1
        idx2word = {index: word for  word,index in word2idx.items()} # 建立一个id到字的字典
        # if(os.path.exists('./checkpoint_test/word2id.pkl')):
        #     pass
        # else:
        #     word2idx_file =




        pickle.dump((word2idx, idx2word),open("./checkpoint/word2id.pkl", "wb")) # 写进去word2id.pkl文件中

    return word2idx, idx2word # 返回 实体到id id到实体 两个字典


def char_index(p_sentences, h_sentences, maxlen=35):

    word2idx, idx2word = load_char_vocab() # 拿到 实体到id id到实体 两个字典

    p_list, h_list = [], []
    for p_sentence, h_sentence in zip(p_sentences, h_sentences):
        # 原词和规范词都转成 字1id 字2id 字3id 的形式
        p = [word2idx[word.lower()] for word in str(p_sentence) if len(word.strip()) > 0 and word.lower() in word2idx.keys()]
        h = [word2idx[word.lower()] for word in str(h_sentence) if len(word.strip()) > 0 and word.lower() in word2idx.keys()]

        p_list.append(p) # 得到原词id形式
        h_list.append(h) # 得到规范词id形式

    p_list = pad_sequences(p_list, maxlen=maxlen) # 得到填充后的 nb_samples * maxlen 矩阵
    h_list = pad_sequences(h_list, maxlen=maxlen)

    return p_list, h_list # 返回两个填充后的矩阵


def load_char_data(path, data_size=None,maxlen=35): # 加载训练数据

    df = pd.read_csv(path) # 打开给进来的训练数据集 训练集每行有三个数据 sentence1原词 sentence2规范词 label正1负0样本标记
    p = df['sentence1'].values[0:data_size] # 拿到原词
    h = df['sentence2'].values[0:data_size] # 拿到规范词
    label = df['label'].values[0:data_size] # 拿到正负样本标记

    p, h, label = shuffle(p, h, label) # 转成元组？

    # [1,2,3,4,5] [4,1,5,2,0]
    p_c_index, h_c_index = char_index(p, h,maxlen=maxlen) # 得到两个填充后的矩阵

    return p_c_index, h_c_index, label # 返回两个填充后的矩阵和正负样本标记


if __name__ == '__main__':

    gen_training_data("./yidu-n7k") # 指定文件夹
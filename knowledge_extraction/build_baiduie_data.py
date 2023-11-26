import sys
import json
from tqdm import tqdm
import codecs
import numpy as np
import pandas as pd 

# 把百度信息抽取竞赛的数据改成模型数据需要的格式
raw_data_dir, training_data_dir = './baiduie', './baiduie_training_data' # 原始数据文件夹 处理后所放文件夹

RANDOM_SEED = 2021

rel_set = set()

text_len = []

train_data = []
i = 0
with open(raw_data_dir + '/train_data/train_data.json', encoding='utf8') as f: # 处理训练集
    for l in tqdm(f.readlines()):
        a = json.loads(l)
        if i == 0:
            print('\n' + '原数据格式' + '\n' + json.dumps(a, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))
            # 打印百度原始数据的格式
        if not a['spo_list']:
            continue
        
        triple_list = []
        for spo in a['spo_list']:
            s = spo['subject'] # 主语 如：邪少兵王
            p = spo['predicate'] # 谓语 如：作者
            o_dict = spo['object'] # {"谓语子类型":"宾语",...} 如：@value:冰火未央
            for k in o_dict.keys(): # 每一个谓语子类型
                triple_list.append((s,p+'_'+k,o_dict[k]))
                # 主语，谓语_谓语子类型，宾语 如：邪少兵王，作者_@value，冰火未央
                rel_set.add(p+'_'+k) # 记录 谓语_谓语子类型 对

        line = {
                'text': a['text'], # 原文
                'triple_list': triple_list # 原文提取结果
               }
        if i == 0:
            print('\n' + '现数据格式' + '\n' + json.dumps(line, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))
            # 转换后数据的格式
        train_data.append(line) # 记录数据转换结果
        text_len.append((len(a['text']))) # 记录原文长度
        i += 1

df = pd.DataFrame({"text_len":text_len}) # 进度条
print("训练集文本长度统计：\n")
print(df["text_len"].describe())

id2rel = {i:j for i,j in enumerate(sorted(rel_set))} # 去重标id每一种谓语_谓语子类型对
rel2id = {j:i for i,j in id2rel.items()} # 得到谓语_谓语子类型对转id字典

with codecs.open(training_data_dir+'/rel2id.json', 'w', encoding='utf-8') as f:
    json.dump([id2rel, rel2id], f, indent=4, ensure_ascii=False) # 把两个字典写入rel2id文件

with codecs.open(training_data_dir+'/train_triples.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, indent=4, ensure_ascii=False) # 把数据转换结果写入train_triples文件


dev_data = []

with open(raw_data_dir + '/dev_data/dev_data.json', encoding='utf8') as f: # 处理验证集 操作同上
    for l in tqdm(f.readlines()):
        a = json.loads(l)
        if not a['spo_list']:
            continue

        triple_list = []
        for spo in a['spo_list']:
            s = spo['subject']
            p = spo['predicate']
            o_dict = spo['object']
            for k in o_dict.keys():
                triple_list.append((s,p+'_'+k,o_dict[k]))
                rel_set.add(p+'_'+k)

        line = {
                'text': a['text'],
                'triple_list': triple_list
               }
        dev_data.append(line)


dev_len = len(dev_data) # 统计数据处理结果
random_order = list(range(dev_len))
np.random.seed(RANDOM_SEED) # 选择随机种子
np.random.shuffle(random_order) # 使用对应随机种子打乱数据处理结果的前后顺序

test_data = [dev_data[i] for i in random_order[:int(0.5 * dev_len)]] # 打乱顺序后的后一半内容作为测试集
dev_data = [dev_data[i] for i in random_order[int(0.5 * dev_len):]] # 验证集仅为原验证集的前一半内容

with codecs.open(training_data_dir+'/dev_triples.json', 'w', encoding='utf-8') as f:
    json.dump(dev_data, f, indent=4, ensure_ascii=False) # 把数据转换结果写入dev_triples文件

with codecs.open(training_data_dir+'/test_triples.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, indent=4, ensure_ascii=False) # 把数据转换结果写入test_triples文件
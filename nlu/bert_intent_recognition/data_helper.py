import json
import pandas as pd

def gen_training_data(raw_data_path):

    label_list = [line.strip() for line in open('label','r',encoding='utf8')] # 列出了能做的类别 13个
    print(label_list)
    label2id = {label:idx for idx,label in enumerate(label_list)} # 13个类别对应id

    data = []
    with open(raw_data_path,'r',encoding='utf8') as f: # 打开原数据文件
        origin_data = f.read()
        origin_data = eval(origin_data)

    # 处理成 原句 类别 类别的id
    label_set = set() # 建一个空集合用来存放类别
    for item in origin_data:
        text = item["originalText"] # 每一句原句文本

        label_class = item["label_4class"][0].strip("'") # 拿到归属四大类
        if label_class == "其他": # 如果是其他 就单独拿出来
            data.append([text,label_class,label2id[label_class]]) # 原句 其他 其他这个类对应的id
            continue
        label_class = item["label_36class"][0].strip("'") # 如果其他三个大类 就获取小类
        label_set.add(label_class) # 目前有的所有类
        if label_class not in label_list: # 如果小类没在范围内 就跳过
            # label_class = "其他"
            continue
        data.append([text,label_class,label2id[label_class]]) # 如果在范围内 原句 小类 小类对应的id

    print(label_set) # 输出类别集合

    data = pd.DataFrame(data,columns=['text','label_class','label']) # csv文件抬头

    print(data['label_class'].value_counts()) # 统计每一种类别的语句数量

    data['text_len'] = data['text'].map(lambda x: len(x)) # 所有语句的长度 便于确定max_len
    print(data['text_len'].describe())
    import matplotlib.pyplot as plt
    plt.hist(data['text_len'], bins=30, rwidth=0.9, density=True,) # 画一个表
    plt.show()

    del data['text_len']

    data = data.sample(frac=1.0) # 打乱顺序
    train_num = int(0.9*len(data)) # 确定要多少当训练集
    train,test = data[:train_num],data[train_num:] # 划分训练集和测试集
    train.to_csv("train.csv",index=False) # 存储训练集
    test.to_csv("test.csv",index=False) # 存储测试集


def load_data(filename):

    df = pd.read_csv(filename,header=0)
    return df[['text','label']].values

if __name__ == '__main__':

    data_path = "./CMID/CMID.json"
    gen_training_data(data_path)

from data_loader import data_generator, load_data
from model import E2EModel, Evaluate
from utils import extract_items, get_tokenizer, metric
import os, argparse

parser = argparse.ArgumentParser(description='Model Controller')
parser.add_argument('--train', default=True, type=bool, help='to train the HBT model, python run.py --train=True')
parser.add_argument('--dataset_dir', default='../baiduie_training_data', type=str, help='')
args = parser.parse_args()

if __name__ == '__main__':

    # pre-trained bert model config
    # 指定预训练好的参数文件
    bert_model = './bert_weight_files/roberta'
    bert_config_path = bert_model + '/bert_config_rbt3.json'
    bert_vocab_path = bert_model + '/vocab.txt'
    bert_checkpoint_path = bert_model + '/bert_model.ckpt'

    # 指定数据集文件和保存路径
    dataset_dir = args.dataset_dir
    train_path = dataset_dir + '/train_triples.json'
    dev_path = dataset_dir + '/dev_triples.json'
    test_path = dataset_dir + '/test_triples.json'
    rel_dict_path = dataset_dir + '/rel2id.json'
    save_weights_path = 'checkpoint_test/best_model.weights'

    LR = 1e-5
    tokenizer = get_tokenizer(bert_vocab_path)
    # 拿到训练集 验证集 测试集 id转谓语_谓语子类型对 谓语_谓语子类型对转id
    train_data, dev_data, test_data, id2rel, rel2id, num_rels = load_data(train_path, dev_path, test_path, rel_dict_path)
    # 拿到预测主语的模型 拿到预测主语在某谓语下对应宾语的模型 拿到联合训练模型
    subject_model, object_model, hbt_model = E2EModel(bert_config_path, bert_checkpoint_path, LR, num_rels)
    
    if args.train: # 如果是训练
        BATCH_SIZE = 16
        EPOCH = 1
        MAX_LEN = 256
        STEPS = len(train_data) // BATCH_SIZE
        data_manager = data_generator(train_data, tokenizer, rel2id, num_rels, MAX_LEN, BATCH_SIZE) # 规定batch信息
        evaluator = Evaluate(subject_model, object_model, tokenizer, id2rel, dev_data, save_weights_path) # 规定评测和终止信息
        hbt_model.fit_generator(data_manager.__iter__(),
                              steps_per_epoch=STEPS,
                              epochs=EPOCH,
                              callbacks=[evaluator]
                              ) # 开始训练
    else: # 如果是预测
        hbt_model.load_weights(save_weights_path) # 加载保存的最优参数
        test_result_path = 'test_result.json' # 指明测试结果保存文件
        isExactMatch = False
        # 测试 规定输出格式 并评估
        precision, recall, f1_score = metric(subject_model, object_model, test_data, id2rel, tokenizer, isExactMatch, test_result_path)
#        print(f'precision:{0}\trecall:{1}\tf1_score:{2}'.format(round(precision,4),round(recall,4),round(f1_score,4)))
        print('f1: %.4f, precision: %.4f, recall: %.4f\n' % (f1_score, precision, recall))

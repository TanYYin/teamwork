import json
import codecs
import threading
from py2neo import Graph
from tqdm import tqdm 

def print_data_info(data_path):

    triples = []
    i = 0
    with open(data_path,'r',encoding='utf8') as f:
        for line in f.readlines():
            data = json.loads(line)
            print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))
            i += 1
            if i >=5:
                break
    return triples

class MedicalExtractor(object):

    def __init__(self):

        super(MedicalExtractor, self).__init__()
        self.graph = Graph( # 定义neo4j的连接服务
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")

        # 共8类实体节点
        self.drugs = [] # 药品
        self.recipes = [] # 菜谱
        self.foods = [] # 食物
        self.checks = [] # 检查
        self.departments = [] # 科室
        self.producers = [] # 药企
        self.diseases = [] # 疾病
        self.symptoms = [] # 症状

        self.disease_infos = [] # 疾病信息 疾病实体的属性 其他实体没有属性

        # 构建节点实体关系
        self.rels_department = [] # 科室－科室关系
        self.rels_noteat = [] # 疾病－忌吃食物关系
        self.rels_doeat = [] # 疾病－宜吃食物关系
        self.rels_recommandeat = [] # 疾病－推荐吃食物关系
        self.rels_commonddrug = [] # 疾病－通用药品关系
        self.rels_recommanddrug = [] # 疾病－热门药品关系
        self.rels_check = [] # 疾病－检查关系
        self.rels_drug_producer = [] # 厂商－药物关系

        self.rels_symptom = [] # 疾病症状关系
        self.rels_acompany = [] # 疾病并发关系
        self.rels_category = [] # 疾病与科室之间的关系
        
    def extract_triples(self,data_path):

        print("从json文件中转换抽取三元组")
        with open(data_path,'r',encoding='utf8') as f:
            for line in tqdm(f.readlines(),ncols=80): # 循环对每一行的操作
                data_json = json.loads(line) # 加载到json？
                disease_dict = {} # 字符串转字典
                disease = data_json['name'] # 疾病字典的键key
                disease_dict['name'] = disease # 疾病字典名称name键的对应值value
                self.diseases.append(disease) # 疾病字典列表？
                disease_dict['desc'] = '' # 疾病字典描述desc键的对应值value
                disease_dict['prevent'] = '' # 疾病字典预防prevent键的对应值value
                disease_dict['cause'] = '' # 疾病字典病因cause键的对应值value
                disease_dict['easy_get'] = '' # 疾病字典易患人群easy_get键的对应值value
                disease_dict['cure_department'] = '' # 疾病字典治疗科室cure_department键的对应值value
                disease_dict['cure_way'] = '' # 疾病字典治疗方法cure_way键的对应值value
                disease_dict['cure_lasttime'] = '' # 疾病字典疗程cure_lasttime键的对应值value
                disease_dict['symptom'] = '' # 疾病字典症状symptom键的对应值value
                disease_dict['cured_prob'] = '' # 疾病字典病愈率cured_prob键的对应值value

                if 'symptom' in data_json: # 如果有提到疾病的症状
                    self.symptoms += data_json['symptom'] # 增加症状节点
                    for symptom in data_json['symptom']: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_symptom.append([disease,'has_symptom', symptom]) # 创建一个疾病-有-症状关系三元组

                if 'acompany' in data_json: # 如果有提到疾病的并发症
                    for acompany in data_json['acompany']: # 疾病字典并发症acompany键的对应值value就是提到疾病的并发症
                        self.rels_acompany.append([disease,'acompany_with', acompany]) # 创建一个疾病—并发有—并发症关系三元组
                        self.diseases.append(acompany) # 增加并发症节点

                if 'desc' in data_json: # 如果有提到疾病的描述
                    disease_dict['desc'] = data_json['desc'] # 疾病字典描述desc键的对应值value就是提到疾病的描述

                if 'prevent' in data_json: # 如果有提到疾病的预防
                    disease_dict['prevent'] = data_json['prevent'] # 疾病字典预防prevent键的对应值value就是提到疾病的预防

                if 'cause' in data_json: # 如果有提到疾病的病因
                    disease_dict['cause'] = data_json['cause'] # 疾病字典病因cause键的对应值value就是提到疾病的病因

                if 'get_prob' in data_json: # 如果有提到疾病的患病率
                    disease_dict['get_prob'] = data_json['get_prob'] # 疾病字典患病率get_prob键的对应值value就是提到疾病的患病率

                if 'easy_get' in data_json: # 如果有提到疾病的易患人群
                    disease_dict['easy_get'] = data_json['easy_get'] # 疾病字典易患人群easy_get键的对应值value就是提到疾病的患病率

                if 'cure_department' in data_json: # 如果有提到疾病的治疗科室
                    cure_department = data_json['cure_department'] # 疾病的治疗科室列表
                    if len(cure_department) == 1: # 如果提到的治疗科室只有一个
                         self.rels_category.append([disease, 'cure_department',cure_department[0]]) # 创建一个疾病—治疗科室-科室关系三元组
                    if len(cure_department) == 2: # 如果提到的治疗科室有两个
                        big = cure_department[0]
                        small = cure_department[1]
                        self.rels_department.append([small,'belongs_to', big]) # 创建一个科室-属于-科室关系三元组
                        self.rels_category.append([disease,'cure_department', small]) # 创建第二个疾病—治疗科室-科室关系三元组

                    disease_dict['cure_department'] = cure_department # 疾病字典并发症acompany
                    self.departments += cure_department # 增加科室节点

                if 'cure_way' in data_json: # 如果有提到疾病的治疗方法
                    disease_dict['cure_way'] = data_json['cure_way'] # 疾病字典治疗方法cure_way键的对应值value就是提到疾病的治疗方法

                if 'cure_lasttime' in data_json: # 如果有提到疾病的疗程
                    disease_dict['cure_lasttime'] = data_json['cure_lasttime'] # 疾病字典疗程cure_lasttime键的对应值value就是提到疾病的疗程

                if 'cured_prob' in data_json: # 如果有提到疾病的病愈率
                    disease_dict['cured_prob'] = data_json['cured_prob'] # 疾病字典病愈率cured_prob键的对应值value就是提到疾病的病愈率

                if 'common_drug' in data_json: # 如果有提到疾病的通用药物
                    common_drug = data_json['common_drug'] # 疾病的通用药物列表
                    for drug in common_drug: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_commonddrug.append([disease,'has_common_drug', drug]) # 创建一个疾病-通用-药物关系三元组
                    self.drugs += common_drug # 增加药物节点

                if 'recommand_drug' in data_json: # 如果有提到疾病的热门药物
                    recommand_drug = data_json['recommand_drug'] # 疾病的热门药物列表
                    self.drugs += recommand_drug # 增加药物节点
                    for drug in recommand_drug: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_recommanddrug.append([disease,'recommand_drug', drug]) # 创建一个疾病-热门-药物关系三元组

                if 'not_eat' in data_json: # 如果有提到疾病的忌口
                    not_eat = data_json['not_eat'] # 疾病的忌口列表
                    for _not in not_eat: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_noteat.append([disease,'not_eat', _not]) # 创建一个疾病-忌口-食物关系三元组

                    self.foods += not_eat # 增加食物节点
                    do_eat = data_json['do_eat'] # 疾病的食物列表
                    for _do in do_eat: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_doeat.append([disease,'do_eat', _do]) # 创建一个疾病-宜吃-食物关系三元组

                    self.foods += do_eat # 增加食物节点

                if 'recommand_eat' in data_json: # 如果有提到疾病的推荐吃食物
                    recommand_eat = data_json['recommand_eat'] # 疾病的推荐吃食物列表
                    for _recommand in recommand_eat: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_recommandeat.append([disease,'recommand_recipes', _recommand]) # 创建一个疾病-推荐吃-食物关系三元组
                    self.recipes += recommand_eat # 增加菜谱节点

                if 'check' in data_json: # 如果有提到疾病的检查
                    check = data_json['check'] # 疾病的检查列表
                    for _check in check: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        self.rels_check.append([disease, 'need_check', _check]) # 创建一个疾病-检查-科目关系三元组
                    self.checks += check # 增加检查节点

                if 'drug_detail' in data_json: # 如果有提到疾病的药物药企
                    for det in data_json['drug_detail']: # 在data_json里面是以列表作为字典的值 所以需要一项一项的拿出来然后
                        det_spilt = det.split('(') # 在data_json里面是药企（药物） 以（分割开药企和药物的名称
                        if len(det_spilt) == 2: # 如果有提及到药企
                            p,d = det_spilt # 左侧是药企名称 右侧是药物名称
                            d = d.rstrip(')') # 去掉药物名称中多余的）
                            if p.find(d) > 0: # 如果药企名称里面有药物的名称
                                p = p.rstrip(d) # 去掉药企名称中多余的药物名称
                            self.producers.append(p) # 增加药企节点
                            self.drugs.append(d) # 增加药物节点
                            self.rels_drug_producer.append([p,'production',d]) # 创建一个药企-生产-药物关系三元组
                        else: # 如果没有提及到药企
                            d = det_spilt[0]
                            self.drugs.append(d) # 增加药物节点

                self.disease_infos.append(disease_dict) # 增加疾病信息节点

    def write_nodes(self,entitys,entity_type): # 在neo4j中创建一种类型的节点的方法

        print("写入 {0} 实体".format(entity_type)) # 创建哪种类型的节点
        for node in tqdm(set(entitys),ncols=80): # 类型中的每个节点 进度条
            cql = """MERGE(n:{label}{{name:'{entity_name}'}})""".format(
                label=entity_type,entity_name=node.replace("'",""))
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)
        
    def write_edges(self,triples,head_type,tail_type): # 在neo4j中创建一种类型的关系的方法

        print("写入 {0} 关系".format(triples[0][1])) # 创建哪种类型的关系
        for head,relation,tail in tqdm(triples,ncols=80): # 类型中的每条关系
            cql = """MATCH(p:{head_type}),(q:{tail_type})
                    WHERE p.name='{head}' AND q.name='{tail}'
                    MERGE (p)-[r:{relation}]->(q)""".format(
                        head_type=head_type,tail_type=tail_type,head=head.replace("'",""),
                        tail=tail.replace("'",""),relation=relation)
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def set_attributes(self,entity_infos,etype): # 在neo4j中添加一种疾病的属性的方法

        print("写入 {0} 实体的属性".format(etype)) # 添加哪种疾病的属性
        for e_dict in tqdm(entity_infos[892:],ncols=80): # 疾病中的每种属性
            name = e_dict['name']
            del e_dict['name']
            for k,v in e_dict.items():
                if k in ['cure_department','cure_way']:
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}={v}""".format(label=etype,name=name.replace("'",""),k=k,v=v)
                else:
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}='{v}'""".format(label=etype,name=name.replace("'",""),k=k,v=v.replace("'","").replace("\n",""))
                try:
                    self.graph.run(cql)
                except Exception as e:
                    print(e)
                    print(cql)


    def create_entitys(self): # 创建全部类型的节点的方法

        self.write_nodes(self.drugs,'药品')
        self.write_nodes(self.recipes,'菜谱')
        self.write_nodes(self.foods,'食物')
        self.write_nodes(self.checks,'检查')
        self.write_nodes(self.departments,'科室')
        self.write_nodes(self.producers,'药企')
        self.write_nodes(self.diseases,'疾病')
        self.write_nodes(self.symptoms,'症状')

    def create_relations(self): # 创建全部类型的关系的方法

        self.write_edges(self.rels_department,'科室','科室')
        self.write_edges(self.rels_noteat,'疾病','食物')
        self.write_edges(self.rels_doeat,'疾病','食物')
        self.write_edges(self.rels_recommandeat,'疾病','菜谱')
        self.write_edges(self.rels_commonddrug,'疾病','药品')
        self.write_edges(self.rels_recommanddrug,'疾病','药品')
        self.write_edges(self.rels_check,'疾病','检查')
        self.write_edges(self.rels_drug_producer,'药企','药品')
        self.write_edges(self.rels_symptom,'疾病','症状')
        self.write_edges(self.rels_acompany,'疾病','疾病')
        self.write_edges(self.rels_category,'疾病','科室')

    def set_diseases_attributes(self): # 添加全部疾病的属性的方法

        # self.set_attributes(self.disease_infos,"疾病")
        t = threading.Thread(target=self.set_attributes,args=(self.disease_infos,"疾病"))
        t.setDaemon(False)
        t.start()


    def export_data(self,data,path): # 输出转存

        if isinstance(data[0],str): # 是否str类型
            data = sorted([d.strip("...") for d in set(data)]) # 去重后排序
        with codecs.open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def export_entitys_relations(self):

        self.export_data(self.drugs,'./graph_data/drugs.json')
        self.export_data(self.recipes,'./graph_data/recipes.json')
        self.export_data(self.foods,'./graph_data/foods.json')
        self.export_data(self.checks,'./graph_data/checks.json')
        self.export_data(self.departments,'./graph_data/departments.json')
        self.export_data(self.producers,'./graph_data/producers.json')
        self.export_data(self.diseases,'./graph_data/diseases.json')
        self.export_data(self.symptoms,'./graph_data/symptoms.json')

        self.export_data(self.rels_department,'./graph_data/rels_department.json')
        self.export_data(self.rels_noteat,'./graph_data/rels_noteat.json')
        self.export_data(self.rels_doeat,'./graph_data/rels_doeat.json')
        self.export_data(self.rels_recommandeat,'./graph_data/rels_recommandeat.json')
        self.export_data(self.rels_commonddrug,'./graph_data/rels_commonddrug.json')
        self.export_data(self.rels_recommanddrug,'./graph_data/rels_recommanddrug.json')
        self.export_data(self.rels_check,'./graph_data/rels_check.json')
        self.export_data(self.rels_drug_producer,'./graph_data/rels_drug_producer.json')
        self.export_data(self.rels_symptom,'./graph_data/rels_symptom.json')
        self.export_data(self.rels_acompany,'./graph_data/rels_acompany.json')
        self.export_data(self.rels_category,'./graph_data/rels_category.json')



if __name__ == '__main__':

    path = "./graph_data/medical.json"
    print_data_info(path) # 打印出数据的形式
    extractor = MedicalExtractor() # 连接neo4j
    extractor.extract_triples(path) # 抽取三元组
    extractor.create_entitys() # 创建实体节点
    extractor.create_relations() # 创建实体关系
    extractor.set_diseases_attributes() # 添加疾病属性
    extractor.export_entitys_relations() # 转存
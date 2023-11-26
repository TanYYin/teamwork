from bert4keras.backend import keras,set_gelu
from bert4keras.models import build_transformer_model
from bert4keras.optimizers import Adam
# bert+textCNN做意图识别

set_gelu('tanh')

def textcnn(inputs,kernel_initializer):

	# 3,4,5
	cnn1 = keras.layers.Conv1D(
			256,
			3, # 卷积核大小
			strides=1, # 步幅
			padding='same', # 输出维度和输入维度一致
			activation='relu',
			kernel_initializer=kernel_initializer
		)(inputs) # shape=[batch_size,maxlen-2,256]
	cnn1 = keras.layers.GlobalMaxPooling1D()(cnn1)  # shape=[batch_size,256] 全局最大池化

	cnn2 = keras.layers.Conv1D(
			256,
			4,
			strides=1,
			padding='same',
			activation='relu',
			kernel_initializer=kernel_initializer
		)(inputs)
	cnn2 = keras.layers.GlobalMaxPooling1D()(cnn2)

	cnn3 = keras.layers.Conv1D(
			256,
			5,
			strides=1,
			padding='same',
			kernel_initializer=kernel_initializer
		)(inputs)
	cnn3 = keras.layers.GlobalMaxPooling1D()(cnn3)

	output = keras.layers.concatenate( # 最后把三个卷积池化的结果进行拼接
		[cnn1,cnn2,cnn3],
		axis=-1)
	output = keras.layers.Dropout(0.2)(output) # 再接一个dropout层
	return output

def build_bert_model(config_path,checkpoint_path,class_nums): # 配置文件路径 预训练文件路径 分类类别的数量

	bert = build_transformer_model( # 模型预加载
		config_path=config_path, 
		checkpoint_path=checkpoint_path, 
		model='bert', 
		return_keras_model=False)

	# [CLS] token1 token2 token3 ... [sep]
	cls_features = keras.layers.Lambda(
		lambda x:x[:,0], # 抽取所有行的第0列
		name='cls-token'
		)(bert.model.output) # shape=[batch_size,768]
	all_token_embedding = keras.layers.Lambda( # 也就是去除第一个CLS和最后一个SEP后剩下的token
		lambda x:x[:,1:-1], # 从第二个到倒数第二个
		name='all-token'
		)(bert.model.output) # shape=[batch_size,maxlen-2,768]
	# 也就是input经过embedding之后的情况

	cnn_features = textcnn( # 将all_token_embedding传给textCNN得到cnn抽取的特征
		all_token_embedding,bert.initializer) # shape=[batch_size,cnn_output_dim]
	concat_features = keras.layers.concatenate( # 经过CNN提取特征后将其和CLS特征进行拼接
		[cls_features,cnn_features],
		axis=-1) # 在最后一个维度进行拼接 最后拼出来的shape为[batch_size,768+cnn_output_dim]

	dense = keras.layers.Dense( # 拼接后接一个全连接层
			units=512, # 输出维度
			activation='relu',
			kernel_initializer=bert.initializer # 权重初始化器
		)(concat_features)

	output = keras.layers.Dense( # 输出层
			units=class_nums, # 分类的类别数量
			activation='softmax', # 激活函数
			kernel_initializer=bert.initializer
		)(dense)

	model = keras.models.Model(bert.model.input,output) # 输入就是bert的输出 输出就是output
	print(model.summary())

	return model

if __name__ == '__main__':

	config_path='./chinese_rbt3_L-3_H-768_A-12/bert_config_rbt3.json'
	checkpoint_path='./chinese_rbt3_L-3_H-768_A-12/bert_model.ckpt'
	class_nums=13
	build_bert_model(config_path, checkpoint_path, class_nums)
import tensorflow as tf
import keras
import numpy as np

from esim import ESIM
from data_helper import load_char_data

np.random.seed(1) # 指定numpy的随机种子
tf.set_random_seed(1) # 指定tensorflow的随机种子

esim_params = { # 参数
    'num_classes':2,
    'max_features':1500,
    'embed_size':200,
    'embedding_matrix':[],
    'w_initializer':'random_uniform',
    'b_initializer':'zeros',
    'dropout_rate':0.2,
    'mlp_activation_func':'relu',
    'mlp_num_layers':1,
    'mlp_num_units':128,
    'mlp_num_fan_out':128,
    'lstm_units':128,
    'input_shapes':[(20,),(20,)],
    'task':'Classification',
}

# 训练的是esim模型
if __name__ == '__main__':

    # char_embedding_matrix = load_char_embed(esim_params['max_features'],esim_params['embed_size'])
    # esim_params['embedding_matrix'] = char_embedding_matrix

    # 调用data_helper的load_char_data函数 得到两个填充后的矩阵和正负样本标记
    p, h, y = load_char_data('./data/train.csv', data_size=None,maxlen=esim_params['input_shapes'][0][0])
    x = [p,h] # 2 * 实体填充矩阵
    y = keras.utils.to_categorical(y,num_classes=esim_params['num_classes']) # 将正负样本标记转换为二进制类矩阵
    p_test, h_test, y_test = load_char_data('./data/test.csv', data_size=None, maxlen=esim_params['input_shapes'][0][0])
    x_test = [p_test, h_test]  # 2 * 实体填充矩阵
    y_test = keras.utils.to_categorical(y_test, num_classes=esim_params['num_classes'])  # 将正负样本标记转换为二进制类矩阵

    model = ESIM(esim_params).build() # 构建模型
    model.compile( # 指定模型的loss函数 优化器 评估指标
        loss='categorical_crossentropy', 
        optimizer='adam', 
        metrics=['accuracy']
        )
    print(model.summary())

    earlystop = keras.callbacks.EarlyStopping( # 提前终止训练的函数
        monitor='val_loss',
        patience=4, 
        verbose=2, 
        mode='min'
        )
    bast_model_filepath = './checkpoint/best_esim_model.h5' # 模型的保存路径
    checkpoint = keras.callbacks.ModelCheckpoint( # 模型的保存函数
        bast_model_filepath, 
        monitor='val_loss', 
        verbose=1, 
        save_best_only=True,
        mode='min'
        )
    model.fit( # 模型的训练函数
        x=x, 
        y=y, 
        batch_size=64, 
        epochs=15, 
        validation_split=0.1, 
        shuffle=True, 
        callbacks=[earlystop,checkpoint]
        )

    model_frame_path = "./checkpoint/esim_model.json" # 模型转json格式后的保存路径
    model_json = model.to_json() # 模型转json格式
    with open(model_frame_path, "w") as json_file:
        json_file.write(model_json) # 保存模型


    # model = keras.models.model_from_json(
    #     open(model_frame_path,"r").read(),
    #     custom_objects=custom_objects
    #     )
    # model.load_weights(bast_model_filepath)
    # model.compile(
    #     loss='categorical_crossentropy', 
    #     optimizer='adam', 
    #     metrics=['accuracy']
    #     )

    loss, acc = model.evaluate(
        x=x_test,
        y=y_test,
        batch_size=128,
        verbose=1
        )
    print("Test loss:",loss, "Test accuracy:",acc)
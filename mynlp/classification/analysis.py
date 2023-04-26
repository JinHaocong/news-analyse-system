import pickle

import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Embedding, Conv1D, MaxPooling1D, Dropout, Flatten, Dense
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.utils import plot_model

from mynlp import seg, normal

"""
要提高模型准确率，您可以尝试调整以下参数：

1，num_words：通过增加 num_words 的值来增加词汇表的大小，可能会提高模型的准确率。但是，这也会导致模型的复杂度增加，需要更多的训练时间和计算资源。
2，embedding_dim：增加 embedding_dim 的值可能会提高模型的准确率，因为更高维度的词嵌入可以捕捉到更多的语义信息。
    但是，同样的，增加 embedding_dim 也会增加模型的复杂度。
3，max_length：通过增加 max_length 的值，您可以允许更长的序列输入，从而提高模型的准确率。但是，同样的，增加 max_length 也会增加模型的复杂度。
4，filters、kernel_size、pool_size：增加卷积层的滤波器个数、卷积核的大小和池化层的大小可能会提高模型的准确率。但是，这也会增加模型的复杂度和训练时间。
5，dense_units：增加全连接层的神经元个数可能会提高模型的准确率。但是，同样的，增加 dense_units 也会增加模型的复杂度。
6，dropout_rate：通过增加 dropout_rate 的值，您可以减少过拟合的风险，从而提高模型的准确率。但是，如果您增加 dropout_rate 的值过高，模型可能会欠拟合。
7，batch_size：增加 batch_size 的值可以加快模型的训练速度，但是，如果 batch_size 的值过大，可能会导致内存不足。
8，epochs：增加 epochs 的值可以提高模型的准确率，但是需要更长的训练时间。
"""


class SentimentAnalysis:
    def __init__(self, model_path, tokenizer_path, positive_path, negative_path, stop_path):
        self.num_words = 5000  # 初始化 Tokenizer 对象时指定的参数，用于控制词汇表的大小，仅保留出现频率最高的 num_words 个词。
        self.embedding_dim = 200  # 词嵌入的维度
        self.max_length = 300  # 输入序列的最大长度
        self.filters = 64  # 卷积层的滤波器个数
        self.kernel_size = 10  # 卷积核的大小
        self.pool_size = 10  # 池化层的大小
        self.dense_units = 500  # 全连接层的神经元个数
        self.dropout_rate = 0.5  # Dropout 层的比例
        self.batch_size = 64  # 批处理大小
        self.epochs = 10  # 训练的轮数
        self.model_path = model_path  # 模型保存的路径
        self.tokenizer_path = tokenizer_path  # Tokenizer 对象保存的路径。
        self.positive_path = positive_path
        self.negative_path = negative_path
        self.stop_path = stop_path
        self.tokenizer = None
        self.model = None
        self.stop_words = set()

        # 尝试加载模型
        try:
            self.model = load_model(model_path)
            self.tokenizer = pickle.load(open(tokenizer_path, "rb"))
        except Exception as error:
            print("初始化；没有找到模型文件，请训练", error)

        with open(self.stop_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.stop_words.add(line.strip())

    def train(self):
        print('train')
        positive_data = []
        negative_data = []
        # 导入数据
        with open(self.positive_path, 'r', encoding='utf-8') as f:
            pos_data = f.readlines()
        with open(self.negative_path, 'r', encoding='utf-8') as f:
            neg_data = f.readlines()

        # 去停用词
        for line in pos_data:
            text = seg.seg(line)
            text = normal.filter_stop(text)
            positive_data.append(text)

        for line in neg_data:
            text = seg.seg(line)
            text = normal.filter_stop(text)
            negative_data.append(text)
            # 将标签转换为0和1
        labels = np.concatenate((np.ones(len(positive_data)), np.zeros(len(negative_data))))

        # 将文本合并并进行标记化
        texts = positive_data + negative_data
        self.tokenizer = Tokenizer(num_words=self.num_words)
        self.tokenizer.fit_on_texts(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)

        # 将序列填充到最大长度
        data = pad_sequences(sequences, maxlen=self.max_length)

        # 打乱数据并划分训练和测试数据集
        indices = np.arange(data.shape[0])
        np.random.shuffle(indices)
        data = data[indices]
        labels = labels[indices]
        num_validation_samples = int(0.2 * data.shape[0])

        x_train = data[:-num_validation_samples]
        y_train = labels[:-num_validation_samples]
        x_test = data[-num_validation_samples:]
        y_test = labels[-num_validation_samples:]

        # 构建卷积神经网络模型
        self.model = Sequential()
        self.model.add(Embedding(self.num_words, self.embedding_dim, input_length=self.max_length))
        self.model.add(Conv1D(filters=self.filters, kernel_size=self.kernel_size, padding='same', activation='relu'))
        self.model.add(MaxPooling1D(pool_size=self.pool_size))
        self.model.add(Dropout(self.dropout_rate))
        self.model.add(Flatten())
        self.model.add(Dense(self.dense_units, activation='relu'))
        self.model.add(Dropout(self.dropout_rate))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.summary()

        # 绘制模型结构到文件
        plot_model(self.model, to_file='model.jpg')

        # 训练模型
        history = self.model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=self.epochs,
                                 batch_size=self.batch_size)
        # verbose 是否显示日志信息，0不显示，1显示进度条，2不显示进度条
        loss, accuracy = self.model.evaluate(x_train, y_train, verbose=1)
        print("训练集：loss {0:.3f}, 准确率：{1:.3f}".format(loss, accuracy))
        loss, accuracy = self.model.evaluate(x_test, y_test, verbose=1)
        print("测试集：loss {0:.3f}, 准确率：{1:.3f}".format(loss, accuracy))

        # 绘制训练曲线
        from matplotlib import pyplot as plt
        pd.DataFrame(history.history).plot(figsize=(8, 5))
        plt.grid(True)
        plt.gca().set_ylim(0, 1)  # set the vertical range to [0-1]
        plt.show()

        # 保存模型
        self.save_model()
        self.save_tokenizer()

    def save_model(self):
        self.model.save(self.model_path)

    def save_tokenizer(self):
        if self.tokenizer is None:
            raise ValueError("Tokenizer not found, please train a model first")
        with open(self.tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_model(self):
        self.model = load_model(self.model_path)

    def load_tokenizer(self):
        with open(self.tokenizer_path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def predict(self, texts):
        if self.model is None:
            raise ValueError("Model not found, please load or train a model")
        test_sequences = self.tokenizer.texts_to_sequences(texts)
        test_data = pad_sequences(test_sequences, maxlen=self.max_length)
        result = np.asscalar(np.float32(self.model.predict(test_data)[0][0]))

        # 判断预测结果
        print(result, 'result')
        if result > 0.5:
            print("该文本的情感倾向为积极")
        else:
            print("该文本的情感倾向为消极")
        return result

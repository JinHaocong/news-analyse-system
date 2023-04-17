# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from mynlp import seg, normal
from mynlp.classification.bayes import Bayes

"""
这段代码实现了一个情感分析模型的训练和使用，通过朴素贝叶斯算法对文本进行分类，判断文本的情感倾向是“正面”还是“负面”。
具体来说，这段代码实现了以下功能：

读取文本文件，将文件中的数据进行训练，得到分类器。
将分类器保存到本地文件中。
从本地文件中加载分类器。
对给定的文本进行情感分类，返回分类结果。
"""

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'sentiment.marshal')


class Sentiment(object):

    def __init__(self):
        self.classifier = Bayes()

    def save(self, fname, iszip=True):
        self.classifier.save(fname, iszip)

    def load(self, fname=data_path, iszip=True):
        self.classifier.load(fname, iszip)

    def handle(self, doc):
        words = seg.seg(doc)
        words = normal.filter_stop(words)
        return words

    def train(self, neg_docs, pos_docs):
        data = []
        for sent in neg_docs:
            data.append([self.handle(sent), 'neg'])
        for sent in pos_docs:
            data.append([self.handle(sent), 'pos'])
        self.classifier.train(data)

    def classify(self, sent):
        ret, prob = self.classifier.classify(self.handle(sent))
        if ret == 'pos':
            return prob
        return 1 - prob


classifier = Sentiment()
classifier.load()


def train(neg_file, pos_file):
    neg_docs = codecs.open(neg_file, 'r', 'utf-8').readlines()
    pos_docs = codecs.open(pos_file, 'r', 'utf-8').readlines()
    global classifier
    classifier = Sentiment()
    classifier.train(neg_docs, pos_docs)


def save(fname, iszip=True):
    classifier.save(fname, iszip)


def load(fname, iszip=True):
    classifier.load(fname, iszip)


def classify(sent):
    return classifier.classify(sent)


# 训练模型
if __name__ == '__main__':
    train('neg.txt', 'pos.txt')
    save('sentiment.marshal')
    classify('不开心')

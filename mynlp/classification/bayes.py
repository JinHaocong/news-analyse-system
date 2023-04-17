# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import gzip
import marshal
import sys
from math import log, exp

from ..utils.frequency import AddOneProb

"""
1，定义了一个 Bayes 类，包括以下方法：
    init()：初始化对象，设置初始的词典和总计数器。
    save(fname, iszip=True)：将训练好的模型保存到文件中。
    load(fname, iszip=True)：从文件中加载训练好的模型。
    train(data)：使用数据集 data 训练模型。
    classify(x)：使用训练好的模型对新数据进行分类。
2，AddOneProb 类是用来计算每个单词在每个分类中的概率，采用了加一平滑技术。
3，train(data) 方法接收一个数据集，其中每个数据元素包括文本和分类标签。
   在训练过程中，对于每个分类，记录其中的每个单词出现的次数，
   并使用 AddOneProb 计算每个单词在分类中的概率，最后统计每个分类中所有单词出现次数的总和。
4，classify(x) 方法接收一个文本 x，返回该文本所属的分类以及概率。
   对于每个分类，先计算其出现的概率，并在此基础上计算每个单词在该分类中出现的概率，
   并求和。最后选取出现概率最大的分类作为文本的分类，并计算出其概率。
5，这里使用了 log 运算来处理很小的概率，避免了数值下溢问题。
6，在计算分类概率时，对于每个分类 k，分别计算其他分类的概率，求和后得到分母，
   最后计算该分类的概率并与其他分类比较，选择概率最大的分类作为文本的分类。
7，由于在计算分母时可能会出现数值溢出的情况，这里使用了异常处理机制进行处理，当出现 OverflowError 时，将概率设为 0。
8，save() 和 load() 方法使用了 gzip 和 marshal 库，分别用于压缩和序列化对象。
   在 Python 3 中，为了避免与 Python 2 中同名的文件冲突，保存的文件名末尾加上了 '.3' 后缀。
"""


class Bayes(object):

    def __init__(self):
        """初始化对象，设置初始的词典和总计数器"""
        self.d = {}
        self.total = 0

    def save(self, fname, iszip=True):
        """将训练好的模型保存到文件中"""
        print('save')
        d = {}
        d['total'] = self.total
        d['d'] = {}
        for k, v in self.d.items():
            d['d'][k] = v.__dict__
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            marshal.dump(d, open(fname, 'wb'))
        else:
            f = gzip.open(fname, 'wb')
            f.write(marshal.dumps(d))
            f.close()

    def load(self, fname, iszip=True):
        """从文件中加载训练好的模型"""
        print('load')
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            d = marshal.load(open(fname, 'rb'))
        else:
            try:
                f = gzip.open(fname, 'rb')
                d = marshal.loads(f.read())
            except IOError:
                f = open(fname, 'rb')
                d = marshal.loads(f.read())
            f.close()
        self.total = d['total']
        self.d = {}
        for k, v in d['d'].items():
            self.d[k] = AddOneProb()
            self.d[k].__dict__ = v

    def train(self, data):
        """使用数据集 data 训练模型"""
        for d in data:
            c = d[1]
            if c not in self.d:
                self.d[c] = AddOneProb()
            for word in d[0]:
                self.d[c].add(word, 1)
        self.total = sum(map(lambda x: self.d[x].getsum(), self.d.keys()))

    def classify(self, x):
        """使用训练好的模型对新数据进行分类"""
        tmp = {}
        for k in self.d:
            tmp[k] = log(self.d[k].getsum()) - log(self.total)
            for word in x:
                tmp[k] += log(self.d[k].freq(word))
        ret, prob = 0, 0
        for k in self.d:
            now = 0
            try:
                for otherk in self.d:
                    now += exp(tmp[otherk] - tmp[k])
                now = 1 / now
            except OverflowError:
                now = 0
            if now > prob:
                ret, prob = k, now
        print(ret, prob)
        return ret, prob

# -*- coding: utf-8 -*-

'''
Implementation of 'TnT - A Statisical Part of Speech Tagger'
'''
from __future__ import unicode_literals

import gzip
import heapq
import marshal
import sys
from math import log

from . import frequency

"""
这段代码实现了一个统计词性标注器TnT（Trigrams 'n' Tags）。

这个标注器需要进行训练才能标注句子。
在训练阶段，TnT对输入的语料进行分析并生成统计模型，包括：单个词性的频率、相邻两个词性的组合频率、相邻三个词性的组合频率、以及词语和词性的组合频率等信息。
训练完成后，TnT可以利用这些信息进行句子的标注。

具体来说，代码中的TnT类中包含以下成员变量：

N：表示训练时进行平滑的最大词频数，用于防止出现概率为0的情况。
l1、l2、l3：表示用于计算词性转移概率的三个系数。
status：表示出现过的所有词性。
wd：表示每个词和其对应词性的出现次数，用于计算每个词对应各个词性的概率。
eos：表示每个相邻两个词性的组合在句子结尾的出现次数，用于计算以某个词性结尾的句子概率。
eosd：表示每个词性在句子结尾的出现次数，用于计算以某个词性结尾的句子概率。
uni、bi、tri：表示单个词性、相邻两个词性的组合、相邻三个词性的组合在语料中的出现次数，用于计算词性转移概率。
word：表示每个词对应的所有可能词性。
trans：表示每个词性转移的概率对数值，用于标注句子。
在代码中，TnT类中的函数主要包括：

save和load：用于将训练好的模型保存到磁盘或从磁盘中加载已有的模型。
tnt_div：用于计算两个数的除法，避免除数为0的情况。
geteos：用于计算以某个词性结尾的句子概率对数值。
train：用于训练模型，生成所有的统计信息。
tag：用于对输入的句子进行标注，输出每个词语的词性。

TnT算法的整个流程：

1，统计词汇表中每个词在训练集中出现的次数，以及它们在不同的词性标注下出现的次数。
2，基于这些统计数据，计算每个词性标注的概率分布。
3，基于训练集中的句子和词性标注序列，统计每个词性标注对后续词性标注的影响。
    这个统计可以使用N元模型（N-grams）完成，即计算在一个长度为N的上下文中，某个词性标注出现的次数，
    然后将出现的次数除以该上下文中所有词性标注的出现次数之和，得到该词性标注在给定上下文中的条件概率分布。
    在TnT中，使用了二元模型，即计算一个词的词性标注与其前面一个词的词性标注之间的条件概率分布。
4，基于上述统计，得到一个基于HMM的词性标注器。给定一个句子，该词性标注器会计算在所有可能的词性标注序列中，哪个序列的概率最大。这可以使用Viterbi算法来完成。
5，对于一些无法在训练集中找到的单词（即OOV词汇），可以使用一些启发式规则来为其分配词性标注，例如根据前缀、后缀、大小写等特征来决定其词性标注。
6，最后，使用标记后的训练集重新训练模型，得到更好的参数估计。这个过程可以迭代执行，直到模型的性能不再提高。
"""


class TnT(object):

    def __init__(self, N=1000):
        self.N = N
        self.l1 = 0.0
        self.l2 = 0.0
        self.l3 = 0.0
        self.status = set()
        self.wd = frequency.AddOneProb()
        self.eos = frequency.AddOneProb()
        self.eosd = frequency.AddOneProb()
        self.uni = frequency.NormalProb()
        self.bi = frequency.NormalProb()
        self.tri = frequency.NormalProb()
        self.word = {}
        self.trans = {}

    def save(self, fname, iszip=True):
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, set):
                d[k] = list(v)
            elif hasattr(v, '__dict__'):
                d[k] = v.__dict__
            else:
                d[k] = v
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            marshal.dump(d, open(fname, 'wb'))
        else:
            f = gzip.open(fname, 'wb')
            f.write(marshal.dumps(d))
            f.close()

    def load(self, fname, iszip=True):
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
        for k, v in d.items():
            if isinstance(self.__dict__[k], set):
                self.__dict__[k] = set(v)
            elif hasattr(self.__dict__[k], '__dict__'):
                self.__dict__[k].__dict__ = v
            else:
                self.__dict__[k] = v

    def tnt_div(self, v1, v2):
        if v2 == 0:
            return 0
        return float(v1) / v2

    def geteos(self, tag):
        tmp = self.eosd.get(tag)
        if not tmp[0]:
            return log(1.0 / len(self.status))
        return log(self.eos.get((tag, 'EOS'))[1]) - log(self.eosd.get(tag)[1])

    def train(self, data):
        for sentence in data:
            now = ['BOS', 'BOS']
            self.bi.add(('BOS', 'BOS'), 1)
            self.uni.add('BOS', 2)
            for word, tag in sentence:
                now.append(tag)
                self.status.add(tag)
                self.wd.add((tag, word), 1)
                self.eos.add(tuple(now[1:]), 1)
                self.eosd.add(tag, 1)
                self.uni.add(tag, 1)
                self.bi.add(tuple(now[1:]), 1)
                self.tri.add(tuple(now), 1)
                if word not in self.word:
                    self.word[word] = set()
                self.word[word].add(tag)
                now.pop(0)
            self.eos.add((now[-1], 'EOS'), 1)
        tl1 = 0.0
        tl2 = 0.0
        tl3 = 0.0
        for now in self.tri.samples():
            c3 = self.tnt_div(self.tri.get(now)[1] - 1,
                              self.bi.get(now[:2])[1] - 1)
            c2 = self.tnt_div(self.bi.get(now[1:])[1] - 1,
                              self.uni.get(now[1])[1] - 1)
            c1 = self.tnt_div(self.uni.get(now[2])[1] - 1, self.uni.getsum() - 1)
            if c3 >= c1 and c3 >= c2:
                tl3 += self.tri.get(now)[1]
            elif c2 >= c1 and c2 >= c3:
                tl2 += self.tri.get(now)[1]
            elif c1 >= c2 and c1 >= c3:
                tl1 += self.tri.get(now)[1]
        self.l1 = float(tl1) / (tl1 + tl2 + tl3)
        self.l2 = float(tl2) / (tl1 + tl2 + tl3)
        self.l3 = float(tl3) / (tl1 + tl2 + tl3)
        for s1 in self.status | set(('BOS',)):
            for s2 in self.status | set(('BOS',)):
                for s3 in self.status:
                    uni = self.l1 * self.uni.freq(s3)
                    bi = self.tnt_div(self.l2 * self.bi.get((s2, s3))[1],
                                      self.uni.get(s2)[1])
                    tri = self.tnt_div(self.l3 * self.tri.get((s1, s2, s3))[1],
                                       self.bi.get((s1, s2))[1])
                    self.trans[(s1, s2, s3)] = log(uni + bi + tri)

    def tag(self, data):
        now = [(('BOS', 'BOS'), 0.0, [])]
        for w in data:
            stage = {}
            samples = self.status
            if w in self.word:
                samples = self.word[w]
            for s in samples:
                wd = log(self.wd.get((s, w))[1]) - log(self.uni.get(s)[1])
                for pre in now:
                    p = pre[1] + wd + self.trans[(pre[0][0], pre[0][1], s)]
                    if (pre[0][1], s) not in stage or p > stage[(pre[0][1],
                                                                 s)][0]:
                        stage[(pre[0][1], s)] = (p, pre[2] + [s])
            stage = list(map(lambda x: (x[0], x[1][0], x[1][1]), stage.items()))
            now = heapq.nlargest(self.N, stage, key=lambda x: x[1])
        now = heapq.nlargest(1, stage, key=lambda x: x[1] + self.geteos(x[0][1]))
        return zip(data, now[0][2])

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

"""
实现了 BM25（Okapi BM25）算法，用于计算文档之间的相似度。
BM25 是一种经典的信息检索（Information Retrieval）算法，用于评估查询与文档之间的匹配程度。
BM25 可以被用来计算一个查询与文档集合中每个文档之间的相关性得分，从而对文档进行排序，以便于返回最相关的文档。

1，初始化参数
    D：文档集合中文档的总数；
    avgdl：文档集合中每篇文档的平均长度；
    docs：文档集合；
    f：文档集合中每篇文档中每个词的出现次数；
    df：文档集合中每个词出现的文档数；
    idf：文档集合中每个词的逆文档频率；
    k1：BM25算法中的一个参数；
    b：BM25算法中的一个参数。

2，初始化函数 init() 会对输入的文档进行处理，包括计算每个文档中每个词的出现频率，每个词在多少个文档中出现过（df），以及每个词的逆文档频率（idf）。

3，计算文档相似度函数 sim() 接受两个参数，一个是查询语句（doc），另一个是待比较的文档索引（index）。
    该函数会计算查询语句与指定文档之间的相似度得分，并返回该得分。

4，计算一个查询与文档集合中所有文档相似度的函数 simall() 接受一个参数，即查询语句（doc）。该函数会对所有文档计算相似度得分，并返回得分列表。




jinhaocong@outlook.com
说完了吗
"""


class BM25(object):

    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = sum([len(doc) + 0.0 for doc in docs]) / self.D
        self.docs = docs
        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for word in doc:
                if not word in tmp:
                    tmp[word] = 0
                tmp[word] += 1
            self.f.append(tmp)
            for k, v in tmp.items():
                if k not in self.df:
                    self.df[k] = 0
                self.df[k] += 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D - v + 0.5) - math.log(v + 0.5)

    def sim(self, doc, index):
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.docs[index])
            score += (self.idf[word] * self.f[index][word] * (self.k1 + 1)
                      / (self.f[index][word] + self.k1 * (1 - self.b + self.b * d
                                                          / self.avgdl)))
        return score

    def simall(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores

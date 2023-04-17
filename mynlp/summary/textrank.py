# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..sim.bm25 import BM25

"""
实现了基于TextRank算法的关键词抽取和文本摘要功能。
其中TextRank类和KeywordTextRank类分别用于处理文本和关键词。

TextRank类计算每篇文档的BM25相似性得分，并将其作为权重构建图，并使用TextRank算法迭代求解图中节点的权重得分。
    得分最高的节点被认为是最重要的节点，从而实现文本摘要的目的。

KeywordTextRank类将每个单词作为节点，并使用TextRank算法计算每个单词的权重得分，得分最高的单词被认为是关键词，从而实现关键词抽取的目的。


TextRank类接受一组文档作为输入，其中每个文档是一个由单词或词语组成的列表。
    在初始化过程中，它使用BM25算法计算文档之间的相似度，并将其用作权重计算中的因子。
    然后，它通过迭代计算每个单词或词语在文本中的重要性得分，根据得分对文档进行排名，返回排名最高的文档作为摘要。

KeywordTextRank类同样接受一组文档作为输入，其中每个文档是一个由单词或词语组成的列表。
    它将每个单词视为一个节点，并根据它们在同一文档中的共现关系构建节点之间的图。
    在初始化过程中，它为每个单词分配初始得分，然后通过迭代计算每个单词的得分，
    考虑到其在文档中出现的频率和与其他单词的关系，返回得分最高的单词作为关键词。
"""


class TextRank(object):

    def __init__(self, docs):
        self.docs = docs
        self.bm25 = BM25(docs)
        self.D = len(docs)
        self.d = 0.85
        self.weight = []
        self.weight_sum = []
        self.vertex = []
        self.max_iter = 200
        self.min_diff = 0.001
        self.top = []

    def solve(self):
        for cnt, doc in enumerate(self.docs):
            scores = self.bm25.simall(doc)
            self.weight.append(scores)
            self.weight_sum.append(sum(scores) - scores[cnt])
            self.vertex.append(1.0)
        for _ in range(self.max_iter):
            m = []
            max_diff = 0
            for i in range(self.D):
                m.append(1 - self.d)
                for j in range(self.D):
                    if j == i or self.weight_sum[j] == 0:
                        continue
                    m[-1] += (self.d * self.weight[j][i]
                              / self.weight_sum[j] * self.vertex[j])
                if abs(m[-1] - self.vertex[i]) > max_diff:
                    max_diff = abs(m[-1] - self.vertex[i])
            self.vertex = m
            if max_diff <= self.min_diff:
                break
        self.top = list(enumerate(self.vertex))
        self.top = sorted(self.top, key=lambda x: x[1], reverse=True)

    def top_index(self, limit):
        return list(map(lambda x: x[0], self.top))[:limit]

    def top(self, limit):
        return list(map(lambda x: self.docs[x[0]], self.top))


class KeywordTextRank(object):

    def __init__(self, docs):
        self.docs = docs
        self.words = {}
        self.vertex = {}
        self.d = 0.85
        self.max_iter = 200
        self.min_diff = 0.001
        self.top = []

    def solve(self):
        for doc in self.docs:
            que = []
            for word in doc:
                if word not in self.words:
                    self.words[word] = set()
                    self.vertex[word] = 1.0
                que.append(word)
                if len(que) > 5:
                    que.pop(0)
                for w1 in que:
                    for w2 in que:
                        if w1 == w2:
                            continue
                        self.words[w1].add(w2)
                        self.words[w2].add(w1)
        for _ in range(self.max_iter):
            m = {}
            max_diff = 0
            tmp = filter(lambda x: len(self.words[x[0]]) > 0,
                         self.vertex.items())
            tmp = sorted(tmp, key=lambda x: x[1] / len(self.words[x[0]]))
            for k, v in tmp:
                for j in self.words[k]:
                    if k == j:
                        continue
                    if j not in m:
                        m[j] = 1 - self.d
                    m[j] += (self.d / len(self.words[k]) * self.vertex[k])
            for k in self.vertex:
                if k in m and k in self.vertex:
                    if abs(m[k] - self.vertex[k]) > max_diff:
                        max_diff = abs(m[k] - self.vertex[k])
            self.vertex = m
            if max_diff <= self.min_diff:
                break
        self.top = list(self.vertex.items())
        self.top = sorted(self.top, key=lambda x: x[1], reverse=True)

    def top_index(self, limit):
        return list(map(lambda x: x[0], self.top))[:limit]

    def top(self, limit):
        return list(map(lambda x: self.docs[x[0]], self.top))

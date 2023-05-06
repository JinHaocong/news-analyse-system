# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mynlp.sim.bm25 import BM25

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

    def __init__(self, text_list):
        self.text_list = text_list  # 包含待提取关键词的文本列表
        self.bm25 = BM25(text_list)  # BM25算法
        self.D = len(text_list)  # 文本列表的长度
        self.d = 0.85  # TextRank算法的阻尼系数，默认为0.85。
        self.weight = []  # 文本相似度矩阵，即每个文本与其他文本之间的相似度。
        self.weight_sum = []  # 每个文本的相似度之和，用于计算TextRank算法的分数。
        self.vertex = []  # 每个文本在TextRank算法中的初始分数，初始值为1.0。
        self.max_iter = 2000  # TextRank算法的最大迭代次数，默认为2000。
        self.min_diff = 0.0001  # TextRank算法的最小收敛差异，默认为0.0001。
        self.top = []

    def solve(self):
        for cnt, text in enumerate(self.text_list):
            # 计算出当前text与text_list中所有的相似度
            scores = self.bm25.simall(text)
            self.weight.append(scores)

            # 排除于自己的相似度并求和
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
                    m[-1] += (self.d * self.weight[j][i] / self.weight_sum[j] * self.vertex[j])
                if abs(m[-1] - self.vertex[i]) > max_diff:
                    max_diff = abs(m[-1] - self.vertex[i])
            self.vertex = m
            if max_diff <= self.min_diff:
                break
        self.top = list(enumerate(self.vertex))
        self.top = sorted(self.top, key=lambda x: x[1], reverse=True)

    def top_index(self, limit):
        return list(map(lambda x: x[0], self.top))[:limit]

    def top_list(self, limit):
        return list(map(lambda x: self.text_list[x[0]], self.top))[:limit]


"""
初始化类的参数，包括文档列表 docs，词典 words，顶点列表 vertex，以及其他参数如阻尼系数 d、最大迭代次数 max_iter、最小差异 min_diff 和前 limit 个关键词 top_keywords。

solve 函数实现了算法的核心逻辑。
首先遍历所有文档，对于每个词语，如果不在词典中，则将其加入到词典 words 和顶点列表 vertex 中，同时将其加入一个队列 que 中。
如果队列中词语数量大于 5，弹出队首元素。对于队列中的每对词语，将其相互添加到 words 中。

使用迭代算法计算关键词的权重。在每次迭代中，对于每个关键词，将其在 words 中连接的所有关键词的权重加权平均，并根据阻尼系数进行调整。
计算完成后，将结果与前一次迭代的结果比较，如果差异小于最小差异 min_diff，则认为已经收敛，退出迭代。
最后，将关键词和对应的权重排序，并保存前 limit 个关键词。

top_index 函数和 top 函数用于获取前 limit 个关键词的索引和关键词及其权重。

可以看到，这个类的主要思路是将文本中的词语转换成一个有向图，然后使用迭代算法计算图中每个节点（关键词）的权重。
相比于其他文本排名算法，Keyword-based TextRank 更加注重关键词之间的相互关系，从而得到更加准确的关键词排名结果。
"""


class KeywordTextRank(object):

    def __init__(self, docs):
        self.docs = docs
        self.words = {}
        self.vertex = {}
        self.d = 0.85
        self.max_iter = 2000
        self.min_diff = 0.0001
        self.top_keywards = []

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
        self.top_keywards = list(self.vertex.items())
        self.top_keywards = sorted(self.top_keywards, key=lambda x: x[1], reverse=True)

    def top_index(self, limit):
        """返回索引"""
        return list(map(lambda x: x[0], self.top_keywards))[:limit]

    def top(self, limit):
        """返回关键词及权重"""
        return [(word, weight) for word, weight in self.top_keywards[:limit]]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import gzip
import marshal
import sys
from math import log

from mynlp.utils import frequency

"""
__init__(): 初始化对象。
save(): 保存对象到文件中。
load(): 从文件中加载对象。
div(): 计算两个数的除法，如果除数为0则返回0。
train(): 训练模型，传入的参数data是一个二维列表，其中每个元素是一个二元组(word, tag)。
log_prob(): 返回给定3个字符的概率的对数。
tag(): 返回一个句子中每个字符的标注结果。

类中定义的3个变量self.l1、self.l2、self.l3表示一元、二元、三元模型的权重。
self.status表示标注状态，包括'b'(开始)、'm'(中间)、'e'(结束)、's'(独立成词)。
self.uni、self.bi、self.tri是三个频率统计对象，分别表示一元、二元、三元模型中字符出现的频率。
三个方法add()、freq()、get()分别用于增加频率、获取频率、获取给定元组的频率。
函数samples()返回所有可能的三元元组。函数getsum()返回所有字符的出现次数之和。

在train()方法中，它接受一个列表，其中每个元素是一个句子，每个句子由一系列词语组成。
对于每个句子，它首先初始化一个长度为2的列表 now，用于存储正在处理的三元组；
然后将两个“开始”状态的标记加入到 unigram 和 bigram 的计数中；
接着对于句子中的每个词语，将它和对应的标记加入到 now 中，然后将它们的 unigram、bigram 和 trigram 的计数都加一。
最后，它利用计算好的频率信息计算出每个状态的权重（l1、l2 和 l3）。

在log_prob()方法中，根据三元模型的概率公式计算概率的对数。它首先分别计算出单字、双字和三字的概率，然后根据 l1、l2 和 l3 的权重将它们加权求和。
如果给定的三个字符没有在模型中出现过，则返回负无穷。

tag() 函数用于对新数据进行分词。
它首先将前两个“开始”状态的标记加入到 now 中，
然后对于数据中的每个字符，遍历所有状态（即 b、m、e 和 s），计算出它们的概率，并将得分最高的状态和对应的字符加入到 stage 中。
最后，将 stage 中的信息更新到 now 中，并返回最后一个状态的序列（即分词结果）。
"""


class CharacterBasedGenerativeModel(object):

    def __init__(self):
        self.l1 = 0.0
        self.l2 = 0.0
        self.l3 = 0.0
        self.status = ('b', 'm', 'e', 's')  # “开始”、“中间”、“结尾”和“单个字符”
        self.uni = frequency.NormalProb()
        self.bi = frequency.NormalProb()
        self.tri = frequency.NormalProb()

    def save(self, fname, iszip=True):
        d = {}
        for k, v in self.__dict__.items():
            if hasattr(v, '__dict__'):
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
            if hasattr(self.__dict__[k], '__dict__'):
                self.__dict__[k].__dict__ = v
            else:
                self.__dict__[k] = v

    def div(self, v1, v2):
        if v2 == 0:
            return 0
        return float(v1) / v2

    def train(self, data):
        for sentence in data:
            now = [('', 'BOS'), ('', 'BOS')]
            # 初始化计数器
            self.bi.add((('', 'BOS'), ('', 'BOS')), 1)
            self.uni.add(('', 'BOS'), 2)
            for word, tag in sentence:
                now.append((word, tag))
                # 单字频率
                self.uni.add((word, tag), 1)
                # 相邻两字频率
                self.bi.add(tuple(now[1:]), 1)
                # 相邻三字频率
                self.tri.add(tuple(now), 1)
                now.pop(0)
        tl1 = 0.0
        tl2 = 0.0
        tl3 = 0.0
        samples = sorted(self.tri.samples(), key=lambda x: self.tri.get(x)[1])
        for now in samples:

            # 三元组的频率/三元组前两位组成的二元组的频率
            c3 = self.div(self.tri.get(now)[1] - 1, self.bi.get(now[:2])[1] - 1)

            # 三元组后两位的频率/三元组第二位的频率
            c2 = self.div(self.bi.get(now[1:])[1] - 1, self.uni.get(now[1])[1] - 1)

            # 三元组最后一位频率/所有频率
            c1 = self.div(self.uni.get(now[2])[1] - 1, self.uni.getsum() - 1)

            if c3 >= c1 and c3 >= c2:
                tl3 += self.tri.get(now)[1]
            elif c2 >= c1 and c2 >= c3:
                tl2 += self.tri.get(now)[1]
            elif c1 >= c2 and c1 >= c3:
                tl1 += self.tri.get(now)[1]
        self.l1 = self.div(tl1, tl1 + tl2 + tl3)
        self.l2 = self.div(tl2, tl1 + tl2 + tl3)
        self.l3 = self.div(tl3, tl1 + tl2 + tl3)

    def log_prob(self, s1, s2, s3):
        """计算概率"""
        uni = self.l1 * self.uni.freq(s3)
        bi = self.div(self.l2 * self.bi.get((s2, s3))[1], self.uni.get(s2)[1])
        tri = self.div(self.l3 * self.tri.get((s1, s2, s3))[1],
                       self.bi.get((s1, s2))[1])
        if uni + bi + tri == 0:
            return float('-inf')
        return log(uni + bi + tri)

    def tag(self, data):
        now = [((('', 'BOS'), ('', 'BOS')), 0.0, [])]
        for w in data:
            stage = {}
            not_found = True
            for s in self.status:
                if self.uni.freq((w, s)) != 0:
                    not_found = False
                    break
            if not_found:
                for s in self.status:
                    for pre in now:
                        stage[(pre[0][1], (w, s))] = (pre[1], pre[2] + [s])
                now = list(map(lambda x: (x[0], x[1][0], x[1][1]),
                               stage.items()))
                continue
            for s in self.status:
                for pre in now:
                    p = pre[1] + self.log_prob(pre[0][0], pre[0][1], (w, s))
                    if (not (pre[0][1],
                             (w, s)) in stage) or p > stage[(pre[0][1],
                                                             (w, s))][0]:
                        stage[(pre[0][1], (w, s))] = (p, pre[2] + [s])
            now = list(map(lambda x: (x[0], x[1][0], x[1][1]), stage.items()))
        return zip(data, max(now, key=lambda x: x[1])[2])

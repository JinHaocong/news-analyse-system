# -*- coding: utf-8 -*-

from . import good_turing

"""
用于计算概率相关的数值。
其中，BaseProb 是所有类的基类，
NormalProb 和 AddOneProb 类分别实现了普通概率计算和加一平滑的概率计算，
GoodTuringProb 类使用 Good-Turing 平滑算法来计算概率。

这些类都有一个 add 方法，用于添加一个 key 和对应的 value（即这个 key 出现的次数），另外还有一些方法可以获取 key 对应的出现次数或概率等信息。
其中，NormalProb 和 AddOneProb 类的实现比较简单，直接对每个 key 的出现次数进行统计，并在需要计算概率时除以总的样本数即可。
GoodTuringProb 类的实现稍微复杂一些，它需要先对所有 key 的出现次数进行处理，再计算概率。
Good-Turing 平滑算法可以处理未出现过的 key，避免了概率为零的情况。
在处理概率前需要先调用 add 方法添加所有的 key 和对应的 value，然后才能使用 get 方法来获取 key 对应的概率。
"""


class BaseProb(object):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 0

    def exists(self, key):
        return key in self.d

    def getsum(self):
        return self.total

    def get(self, key):
        if not self.exists(key):
            return False, self.none
        return True, self.d[key]

    def freq(self, key):
        return float(self.get(key)[1]) / self.total

    def samples(self):
        return self.d.keys()


class NormalProb(BaseProb):

    def add(self, key, value):
        if not self.exists(key):
            self.d[key] = 0
        self.d[key] += value
        self.total += value


class AddOneProb(BaseProb):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 1

    def add(self, key, value):
        self.total += value
        if not self.exists(key):
            self.d[key] = 1
            self.total += 1
        self.d[key] += value


class GoodTuringProb(BaseProb):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.handled = False

    def add(self, key, value):
        if not self.exists(key):
            self.d[key] = 0
        self.d[key] += value

    def get(self, key):
        if not self.handled:
            self.handled = True
            tmp, self.d = good_turing.main(self.d)
            self.none = tmp
            self.total = sum(self.d.values()) + 0.0
        if not self.exists(key):
            return False, self.none
        return True, self.d[key]

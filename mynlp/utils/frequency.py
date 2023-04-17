# -*- coding: utf-8 -*-

from . import good_turing

"""
定义了三个概率计算的类：BaseProb、NormalProb、AddOneProb、GoodTuringProb。

这些类用于处理概率相关的计算，每个类都有一个 add 方法，用于添加一个 key 和对应的 value（即这个 key 出现的次数），
另外还有一些方法可以获取 key 对应的出现次数或概率等信息。

其中，NormalProb 和 AddOneProb 类分别实现了普通的概率计算和加一平滑的概率计算。
    GoodTuringProb 类使用了 Good-Turing 平滑算法来计算概率，
        需要在处理概率前先调用 add 方法添加所有的 key 和对应的 value，然后才能使用 get 方法来获取 key 对应的概率。
    Good-Turing 平滑算法可以处理未出现过的 key，避免了概率为零的情况。
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

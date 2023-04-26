# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

"""
SimpleMerge 的类，实现了一种简单的字符串合并算法。
其构造函数 init() 接收两个参数，分别是待处理的字符串 doc 和包含需要合并的词和相应权重的元组列表 words。

merge() 方法是该类的核心方法，它首先创建了一个空字典 trans，用于存储合并后的词及其相应权重。
然后对于每个需要合并的词 w1，使用正则表达式在 doc 中查找所有匹配的子串，计算子串的权重之和 cw。
接着对于其他所有需要合并的词 w2，使用正则表达式在 doc 中查找所有匹配的由 w1 和 w2 组成的子串，
计算子串的权重之和 cnt。如果 cw 小于 cnt 的两倍，说明 w2 更适合作为合并后的词，将 w1 对应的键值对 trans[w1[0]] 修改为 (w2[0], w1[1]+w2[1])。

接下来遍历元组列表 words，对于每个元组，如果其对应的键值不在 trans 中，说明这个词不能被合并，跳过该元组。否则，将这个词与其合并后的字符串一起加入返回结果列表 ret 中。
"""


class SimpleMerge(object):
    def __init__(self, doc, words):
        self.doc = doc
        self.words = words

    def merge(self):
        trans = {}
        for w in self.words:
            trans[w[0]] = ('', w[1])
        for w1 in self.words:
            cw = 0
            lw = len(w1[0])
            pattern = re.compile(w1[0])
            for match in pattern.findall(self.doc):
                cw += w1[1]
            for w2 in self.words:
                cnt = 0
                l2 = len(w1[0]) + len(w2[0])
                pattern = re.compile(w1[0] + w2[0])
                for match in pattern.findall(self.doc):
                    cnt += w2[1]
                if cw < cnt * 2:
                    trans[w1[0]] = (w2[0], w1[1] + w2[1])
                    break
        ret = []
        for w in self.words:
            if w[0] not in trans:
                continue
            s = ''
            weight = trans[w[0]][1]
            now = trans[w[0]][0]
            while now:
                s += now
                weight += w[1]
                if now not in trans:
                    break
                tmp = trans[now]
                del trans[now]
                now = tmp[0]
            trans[w[0]] = (s, weight)
        for w in self.words:
            if w[0] in trans:
                ret.append((w[0] + trans[w[0]][0], trans[w[0]][1]))
        return ret

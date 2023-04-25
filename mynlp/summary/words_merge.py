# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

"""
合并算法，将文本中包含的一组指定单词合并成新的单词。
具体来说，它接收两个参数：doc 表示待合并的文本，words 是一个包含待合并单词的列表。
类的 merge 方法将 words 中的每个单词和文本中出现的位置进行比对，尽可能多地找到相邻出现的单词组合，然后返回一个包含这些新单词的列表。
这个合并算法主要用于文本预处理和特征提取中。
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

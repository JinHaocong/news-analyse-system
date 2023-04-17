# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
            trans[w] = ''
        for w1 in self.words:
            cw = 0
            lw = len(w1)
            for i in range(len(self.doc) - lw + 1):
                if w1 == self.doc[i: i + lw]:
                    cw += 1
            for w2 in self.words:
                cnt = 0
                l2 = len(w1) + len(w2)
                for i in range(len(self.doc) - l2 + 1):
                    if w1 + w2 == self.doc[i: i + l2]:
                        cnt += 1
                if cw < cnt * 2:
                    trans[w1] = w2
                    break
        ret = []
        for w in self.words:
            if w not in trans:
                continue
            s = ''
            now = trans[w]
            while now:
                s += now
                if now not in trans:
                    break
                tmp = trans[now]
                del trans[now]
                now = tmp
            trans[w] = s
        for w in self.words:
            if w in trans:
                ret.append(w + trans[w])
        return ret

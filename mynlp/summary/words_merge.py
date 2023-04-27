# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from mynlp.utils.trie import Trie

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
        self.trie = Trie()  # 初始化 Trie 类

        # 将关键字插入 Trie 中
        for word in words:
            self.trie.insert(word[0], word[1])

    def merge(self):
        trans = {}

        # 遍历 Trie，查找关键字
        for word in self.words:
            value = self.trie.find(word[0])
            if value is not None:
                trans[word[0]] = ('', value[1])

        for word1 in self.words:
            cw = 0
            lw = len(word1[0])
            pattern = re.compile(word1[0])
            for match in pattern.findall(self.doc):
                cw += word1[1]

            for word2 in self.words:
                cnt = 0
                l2 = len(word1[0]) + len(word2[0])
                pattern = re.compile(word1[0] + word2[0])
                for match in pattern.findall(self.doc):
                    cnt += word2[1]
                if cw < cnt * 2:
                    value = self.trie.find(word2[0])
                    if value is not None:
                        trans[word1[0]] = (word2[0], word1[1] + value[1])
                        break

        ret = []
        for word in self.words:
            if word[0] not in trans:
                continue
            s = ''
            weight = trans[word[0]][1]
            now = trans[word[0]][0]
            while now:
                s += now
                weight += word[1]
                if now not in trans:
                    break
                tmp = trans[now]
                del trans[now]
                now = tmp[0]
            trans[word[0]] = (s, weight)

        for word in self.words:
            if word[0] in trans:
                ret.append((word[0] + trans[word[0]][0], trans[word[0]][1]))
        return ret

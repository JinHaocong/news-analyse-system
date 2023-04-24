# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs

from mynlp.utils.trie import Trie

"""
这段代码定义了一个 PinYin 类，其主要功能是将中文字符串转换为对应的拼音。
具体来说，它使用了一个自定义的 Trie 数据结构（即字典树）来存储拼音词典，其中每个节点表示一个拼音音节。该类有两个方法：

1，__init__(self, fname): 这个方法是类的构造函数，接受一个文件名作为输入参数，用于加载拼音词典。
    它打开一个指定的文本文件，每行以空格分隔为一个中文词和它的拼音音节列表。然后将这些数据插入到字典树中，以便在后续的查询中使用。

2，get(self, text): 这个方法接受一个中文字符串作为输入，将其转换为对应的拼音列表。
    它首先通过 Trie 数据结构进行文本匹配，找到对应的拼音音节列表，然后将它们合并成一个拼音列表返回。

需要注意的是，该类依赖于一个自定义的 Trie 类，并使用了 Python 的 codecs 库来处理中文编码问题。
"""


class PinYin(object):

    def __init__(self, fname):
        self.handle = Trie()
        fr = codecs.open(fname, 'r', 'utf-8')
        for line in fr:
            words = line.split()
            self.handle.insert(words[0], words[1:])
        fr.close()

    def get(self, text):
        ret = []
        for i in self.handle.translate(text):
            if isinstance(i, list) or isinstance(i, tuple):
                ret = ret + i
            else:
                ret.append(i)
        return ret

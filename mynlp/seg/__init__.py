# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

from mynlp.seg import seg as TnTseg

"""
中文分词的功能，采用的是基于隐马尔可夫模型（Hidden Markov Model，简称 HMM）的分词算法。主要涉及的函数有：

1，seg(sent): 这个函数接受一个中文字符串作为输入，将其分词为一个词语列表，并返回。
    它首先使用正则表达式 re_zh 匹配中文字符，然后调用 single_seg 函数对其中的每个中文子串进行分词，最后将所有的分词结果合并成一个词语列表返回。

2，train(fname): 这个函数接受一个文本文件名作为输入，用于训练隐马尔可夫模型。
    它使用了 seg 函数进行分词，并将分词结果传递给 HMM 模型进行训练。

3，save(fname, iszip=True): 这个函数接受一个文件名和一个布尔值作为输入，用于将训练好的模型保存到指定的文件中。
    如果 iszip 参数为 True，则会使用 gzip 压缩进行压缩。

4，load(fname, iszip=True): 这个函数接受一个文件名和一个布尔值作为输入，用于从指定的文件中加载训练好的模型。
    如果 iszip 参数为 True，则会使用 gzip 解压缩进行解压。

5，single_seg(sent): 这个函数接受一个中文字符串作为输入，将其分词为一个词语列表，并返回。
    它使用了 HMM 模型对输入的中文字符串进行分词，并将分词结果以列表的形式返回。
"""

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'seg.marshal')
segger = TnTseg.Seg()
segger.load(data_path, True)
re_zh = re.compile('([\u4E00-\u9FA5]+)')


def seg(sent):
    words = []
    for s in re_zh.split(sent):
        s = s.strip()
        if not s:
            continue
        if re_zh.match(s):
            words += single_seg(s)
        else:
            for word in s.split():
                word = word.strip()
                if word:
                    words.append(word)
    return words


def train(fname):
    global segger
    segger = TnTseg.Seg()
    segger.train(fname)


def save(fname, iszip=True):
    segger.save(fname, iszip)


def load(fname, iszip=True):
    segger.load(fname, iszip)


def single_seg(sent):
    return list(segger.seg(sent))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from ..utils.tnt import TnT

"""
这段代码定义了一些函数和变量，用于基于TnT算法进行中文分词和词性标注。

其中，函数train(fname)用于训练TnT算法的模型，fname为训练数据的文件名。
    函数save(fname, iszip=True)用于将训练好的模型保存到文件中，iszip参数表示是否压缩存储。
    函数load(fname, iszip=True)用于从文件中加载模型。
    函数tag_all(words)接受一个由单词组成的列表words，返回一个由每个单词及其词性组成的元组所组成的列表。
    函数tag(words)则仅返回词性的列表。这两个函数都是基于已经训练好的TnT模型进行的。

该模块的目的是为了方便使用TnT算法对中文文本进行分词和词性标注，提供了训练、保存、加载和标注等功能。
"""

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'tag.marshal')
tagger = TnT()
tagger.load(data_path)


def train(fname):
    fr = codecs.open(fname, 'r', 'utf-8')
    data = []
    for i in fr:
        line = i.strip()
        if not line:
            continue
        tmp = map(lambda x: x.split('/'), line.split())
        data.append(tmp)
    fr.close()
    global tagger
    tagger = TnT()
    tagger.train(data)


def save(fname, iszip=True):
    tagger.save(fname, iszip)


def load(fname, iszip=True):
    tagger.load(fname, iszip)


def tag_all(words):
    return tagger.tag(words)


def tag(words):
    return map(lambda x: x[1], tag_all(words))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os
import re

from . import pinyin
from . import zh

"""
中文文本处理模块，包含以下几个函数；

1，filter_stop(words): 这个函数接受一个字符串列表作为输入，返回过滤掉停用词之后的字符串列表。

2，zh2hans(sent): 这个函数接受一个中文字符串作为输入，返回一个简化的中文字符串。

3，get_sentences(doc): 这个函数接受一个文本字符串作为输入，将其分成句子，返回句子的列表。

4，get_pinyin(sentence): 这个函数接受一个中文字符串作为输入，返回该字符串的拼音列表。其中，中文字符使用正则表达式提取出来，然后使用拼音库进行转换。

此外，这段代码还导入了一些 Python 标准库和自定义库，以及一些文本数据文件。 
具体来说，它导入了 os、re、codecs 库，以及 zh 和 pinyin 两个自定义库。
它还打开了一个停用词文本文件，将其中的词汇加载到一个 set 数据结构中，并将一个拼音文本文件加载到 pinyin.PinYin 对象中。
最后，它定义了一个正则表达式 re_zh，用于提取中文字符。
"""

stop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'stopwords.txt')
pinyin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'pinyin.txt')
stop = set()
fr = codecs.open(stop_path, 'r', 'utf-8')
for word in fr:
    stop.add(word.strip())
fr.close()
pin = pinyin.PinYin(pinyin_path)
re_zh = re.compile('([\u4E00-\u9FA5]+)')


def filter_stop(words):
    return list(filter(lambda x: x not in stop, words))


def zh2hans(sent):
    return zh.transfer(sent)


def get_sentences(doc):
    line_break = re.compile('[\r\n]')
    delimiter = re.compile('[，。？！；]')
    sentences = []
    for line in line_break.split(doc):
        line = line.strip()
        if not line:
            continue
        for sent in delimiter.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences


def get_pinyin(sentence):
    ret = []
    for s in re_zh.split(sentence):
        s = s.strip()
        if not s:
            continue
        if re_zh.match(s):
            ret += pin.get(s)
        else:
            for word in s.split():
                word = word.strip()
                if word:
                    ret.append(word)
    return ret

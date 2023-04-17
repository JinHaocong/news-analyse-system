# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import normal
from . import seg
from . import sentiment
from . import tag
from .sim import bm25
from .summary import textrank
from .summary import words_merge

"""
这段代码实现了一个自然语言处理（NLP）类，包含了常见的文本处理功能，
如分词、句子切分、汉字转化为简体字、获取拼音、情感分析、词性标注、关键词提取、文本相似度计算和摘要提取等。具体功能包括：

初始化时输入待处理的文本，创建 BM25 模型实例。
words：获取文本的分词结果。
sentences：获取文本的句子切分结果。
han：将文本中的繁体汉字转化为简体汉字。
pinyin：获取文本的拼音。
sentiments：对文本进行情感分析，返回情感得分。
tags：对文本进行词性标注，返回每个词及其对应的词性。
tf：获取 BM25 模型中文本中每个词的词频。
idf：获取 BM25 模型中文本中每个词的逆文档频率。
sim：计算输入文本与当前文本之间的相似度。
summary：对文本进行摘要提取，返回指定数量的关键句子。
keywords：对文本进行关键词提取，返回指定数量的关键词。如果 merge 参数为 True，则将关键词进行合并。
"""


class NLP(object):

    def __init__(self, doc):
        self.doc = doc
        self.bm25 = bm25.BM25(doc)

    @property
    def words(self):
        return seg.seg(self.doc)

    @property
    def sentences(self):
        return normal.get_sentences(self.doc)

    @property
    def han(self):
        return normal.zh2hans(self.doc)

    @property
    def pinyin(self):
        return normal.get_pinyin(self.doc)

    @property
    def sentiments(self):
        return sentiment.classify(self.doc)

    @property
    def tags(self):
        words = self.words
        tags = tag.tag(words)
        return zip(words, tags)

    @property
    def tf(self):
        return self.bm25.f

    @property
    def idf(self):
        return self.bm25.idf

    def sim(self, doc):
        return self.bm25.simall(doc)

    def summary(self, limit=5):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = seg.seg(sent)
            words = normal.filter_stop(words)
            doc.append(words)
        rank = textrank.TextRank(doc)
        rank.solve()
        ret = []
        for index in rank.top_index(limit):
            ret.append(sents[index])
        return ret

    def keywords(self, limit=5, merge=False):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = seg.seg(sent)
            words = normal.filter_stop(words)
            doc.append(words)
        rank = textrank.KeywordTextRank(doc)
        rank.solve()
        ret = []
        for w in rank.top_index(limit):
            ret.append(w)
        if merge:
            wm = words_merge.SimpleMerge(self.doc, ret)
            return wm.merge()
        return ret

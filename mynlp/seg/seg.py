# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import codecs

from mynlp.seg.y09_2047 import CharacterBasedGenerativeModel
from mynlp.utils.tnt import TnT

"""
定义 Seg 的类，用于中文分词。该类具有以下方法：

1，__init__(self, name='other'): 初始化方法，根据输入的 name 值选择不同的中文分词模型，
    如果 name 为 tnt，则使用 TnT 模型，否则使用 CharacterBasedGenerativeModel 模型。
2，save(self, fname, iszip=True): 将训练好的模型保存到文件中，fname 为保存的文件名，iszip 为是否使用压缩。
3，load(self, fname, iszip=True): 从文件中加载模型，fname 为模型文件名，iszip 为是否使用压缩。
4，train(self, fname): 训练模型，fname 为训练文件名。
    训练文件中的每一行为一个句子，句子中的每一个词语都带有词性标注，使用斜杠 / 分隔，例如 中文/n 分词/v。
5，seg(self, sentence): 对输入的句子进行分词，并返回分词结果。
"""


class Seg(object):

    def __init__(self, name='other'):
        if name == 'tnt':
            self.segger = TnT()
        else:
            self.segger = CharacterBasedGenerativeModel()

    def save(self, fname, iszip=True):
        self.segger.save(fname, iszip)

    def load(self, fname, iszip=True):
        self.segger.load(fname, iszip)

    def train(self, fname):
        fr = codecs.open(fname, 'r', 'utf-8')
        data = []
        for i in fr:
            line = i.strip()
            if not line:
                continue
            tmp = [x.split('/') for x in line.split()]
            data.append(tmp)
        fr.close()
        self.segger.train(data)

    def seg(self, sentence):
        ret = self.segger.tag(sentence)
        tmp = ''
        result = []
        for i in ret:
            if i[1] == 'e':
                result.append(tmp + i[0])
                tmp = ''
            elif i[1] == 'b' or i[1] == 's':
                if tmp:
                    result.append(tmp)
                tmp = i[0]
            else:
                tmp += i[0]
        if tmp:
            result.append(tmp)
        return result


def seg_test(text):
    my_seg = Seg()
    my_seg.load('seg.marshal')
    print(' '.join(my_seg.seg(text)))


def seg_train(text):
    my_seg = Seg()
    my_seg.train('data.txt')
    my_seg.save('seg.marshal')
    print(' '.join(my_seg.seg(text)))


if __name__ == '__main__':
    seg_train('基于三阶隐马尔可夫模型的中文文本分词算法。')
    seg_test('主要是用来放置一些简单快速的中文分词的程序！')

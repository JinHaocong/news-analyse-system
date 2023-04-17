# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
这段代码实现了一个 Trie 字典树数据结构，并提供了三个方法：

insert(self, key, value)：将字符串 key 插入到 Trie 树中，将 value 作为该字符串的值保存。
find(self, text, start=0)：在 Trie 树中查找以 text[start:] 开头的字符串，返回以该字符串结尾的最长字符串及其对应的值。
    如果该字符串不存在，返回上一个查找到的字符串及其对应的值。
translate(self, text, with_not_found=True)：将字符串 text 中出现在 Trie 树中的所有字符串替换为其对应的值。
    如果 with_not_found 为 True，则未在 Trie 树中找到的字符将原样保留。函数返回替换后的字符串列表。

使用这个 Trie 树，可以实现很多字符串相关的算法和应用，如字符串匹配、自动补全、词性标注等。
"""


class Trie(object):

    def __init__(self):
        self.d = {}

    def insert(self, key, value):
        now = self.d
        for k in key:
            if not k in now:
                now[k] = {}
            now = now[k]
        now['value'] = value

    def find(self, text, start=0):
        now = self.d
        n = len(text)
        ret = None
        pos = start
        while pos < n:
            if text[pos] in now:
                now = now[text[pos]]
            else:
                return ret
            if 'value' in now:
                ret = (text[start:pos + 1], now['value'])
            pos += 1
        return ret

    def translate(self, text, with_not_found=True):
        n = len(text)
        pos = 0
        ret = []
        while pos < n:
            now = self.d
            if text[pos] in now:
                tmp = self.find(text, pos)
                if tmp:
                    ret.append(tmp[1])
                    pos += len(tmp[0])
                    continue
            if with_not_found:
                ret.append(text[pos])
            pos += 1
        return ret

import json
import time

import requests
from django.db import models

from mynlp import NLP


def bai_du_ai(text, result):
    """调用百度AI分析情感接口"""
    try:
        max_length = 1500
        text = text.replace(' ', '').replace('\n', '').replace('\t', '').replace("\u3000", '')
        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.5e32b04f49903cd9e520c7a2be477c78.2592000.1684409657.282335-32554078&charset=UTF-8"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        texts = [text[i: i + max_length] for i in range(0, len(text), max_length)]
        payload = json.dumps({
            "text": texts[0]
        })
        response = requests.request("POST", url, headers=headers, data=payload).json()
        result[0] = response['items'][0]['positive_prob']
        result[1] = response['items'][0]['negative_prob']
        print(response)
        print(result)
        # save_file(text, result)
    except Exception as error:
        print('bai_du_ai函数报错', error)
    return result


def save_file(text, prop):
    pos = open('positive1.txt', 'a', encoding='utf-8')
    neg = open('negative1.txt', 'a', encoding='utf-8')
    if prop[0] > prop[1]:
        # 定义为积极情感
        pos.write(text)
        pos.write('\n')
    else:
        neg.write(text)
        neg.write('\n')
    pos.close()
    neg.close()


def get_all_news():
    news_list = News.objects.all()
    for i in news_list:
        bai_du_ai(i.text, [0, 0])
        time.sleep(0.4)


class News(models.Model):
    docid = models.CharField("新闻id", max_length=255, unique=True)
    url = models.CharField("新闻原链接", max_length=255)
    wapurl = models.CharField("新闻移动版原链接", max_length=255)
    title = models.CharField("标题", max_length=255)
    intro = models.CharField("简介", max_length=255)
    img = models.TextField("封面图")
    images = models.TextField("图片列表")
    keywords = models.CharField("关键词", max_length=255)
    media_name = models.CharField("来源媒体", max_length=255)
    subject = models.CharField("新闻主题", max_length=255)
    text = models.TextField("新闻文本内容")
    html = models.TextField("新闻结构内容")
    intime = models.CharField("发布时间", max_length=255)
    view_count = models.IntegerField("点击率", default=0)

    @classmethod
    def sentiment(cls, text):
        # get_all_news()
        # 情感分析的分析结果
        sentiments = NLP(text).sentiments
        sentiments_model = NLP(text).sentiments_model
        baidu_result = bai_du_ai(text, [0, 0])
        print(sentiments, 'sentiments')
        print(sentiments_model, 'sentiments_model')
        print(baidu_result, 'baidu_result')
        result = [sentiments] * 2
        sentiments_model_result = [sentiments_model] * 2

        result[0] = sentiments
        result[1] = 1 - sentiments
        sentiments_model_result[0] = sentiments_model
        sentiments_model_result[1] = 1 - sentiments_model
        # return bai_du_ai(text, result)
        # return result
        return sentiments_model_result

    class Meta:
        db_table = "news"
        verbose_name = "新闻数据"
        verbose_name_plural = verbose_name

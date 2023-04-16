import requests
from django.db import models
from mynlp import NLP


def mean(arr):
    return sum(arr) / len(arr)


def bd_sentiment(text, result):
    try:
        t = requests.post(
            "https://ai.baidu.com/aidemo",
            data=dict(apiType="nlp", type="sentimentClassify", t1=text),
            headers={
                "Referer": "https://ai.baidu.com/tech/nlp_apply/sentiment_classify"
            },
        ).json()["data"]["items"][0]
        result = [t["positive_prob"], t["negative_prob"]]
    except Exception:
        pass
    return result


def bs_sentiment(text, result):
    try:
        max_length = 500
        texts = [text[i : i + max_length] for i in range(0, len(text), max_length)]
        probs = []
        for i in texts:
            result = requests.post(
                "http://static.bosonnlp.com/analysis/sentiment?analysisType=weibo",
                data=dict(data=i),
            ).json()
            probs.append(result[0])
        result = [mean([i[0] for i in probs]), mean([i[1] for i in probs])]
    except:
        pass
    return result


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
        # 情感分析的分析结果
        sentiments = NLP(text).sentiments
        result = [sentiments] * 2
        if sentiments > 0.5:
            result[1] = 1 - sentiments
        else:
            result[0] = 1 - sentiments
        return bs_sentiment(text, result)

    class Meta:
        db_table = "news"
        verbose_name = "新闻数据"
        verbose_name_plural = verbose_name

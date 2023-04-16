from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponse
from jieba import analyse
from pyecharts import options as opts
from pyecharts.charts import Pie, WordCloud

from .models import *


def to_dict(l, exclude=tuple()):
    # 将数据库模型 变为 字典数据 的工具类函数
    def transform(v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d %H:%M:%S")
        return v

    def _todict(obj):
        j = {
            k: transform(v)
            for k, v in obj.__dict__.items()
            if not k.startswith("_") and k not in exclude
        }
        return j

    return [_todict(i) for i in l]


def get_list(request):
    # News.objects.all().delete()
    # 文本列表
    body = request.json
    pagesize = body.get("pagesize", 50)
    page = body.get("page", 1)
    query = {
        k[1:]: v
        for k, v in body.items()
        if k.startswith("_") and (v != "" and v is not None)
    }
    q = Q(**query)
    objs = News.objects.filter(q).order_by("-intime")
    paginator = Paginator(objs, pagesize)
    pg = paginator.page(page)
    result = to_dict(pg.object_list)
    return JsonResponse({"total": paginator.count, "result": result})


def get_detail(request):
    body = request.json
    id = body.get("id")
    o = News.objects.get(pk=id)
    # 点击率+1
    o.view_count += 1
    o.save()
    return JsonResponse(to_dict([o])[0])


def sentiment(request):
    # 情感分析
    data = request.json
    text = data.get("text")
    try:
        prob = [round(i, 2) for i in News.sentiment(text)]
    except Exception as error:
        print(error)
        prob = [0.5, 0.5]

    return JsonResponse(prob, safe=False)


def pie(request):
    # 文本的正负面概率占比饼图
    data = request.json
    text = data.get("text")
    try:
        prob = [round(i, 2) for i in News.sentiment(text)]
    except Exception as error:
        print(error)
        prob = [0.5, 0.5]
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(["正面指数", "负面指数"], prob)],
            radius=["50%", "70%"],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
        )
        .set_colors(["green", "red"])
        .set_global_opts(
            title_opts=opts.TitleOpts("文本情感分析结果", pos_left="center", pos_bottom=0),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return HttpResponse(c.dump_options(), content_type="aplication/json")


def keywords(request):
    # 文本的关键词分析
    data = request.json
    text = data.get("text")
    keywords = analyse.extract_tags(text, withWeight=True, topK=100)
    c = (
        WordCloud()
        .add("", keywords, word_size_range=[20, 100])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关键词云图", pos_left="center", pos_bottom=0)
        )
    )
    return HttpResponse(c.dump_options(), content_type="aplication/json")


def summary(request):
    # 文本的摘要
    data = request.json
    text = data.get("text")
    return JsonResponse(NLP(text).summary(), safe=False)


def tag(request):
    # 文本的词性分析
    data = request.json
    text = data.get("text")
    result = list(NLP(text).tags)
    return JsonResponse(result, safe=False)

from django.contrib import admin

from .models import *

"""
Django admin配置文件，用于自定义News模型在后台管理中的展示。
该文件定义了一个名为NewsAdmin的类，并将该类注册到了admin.site中，以便在后台管理中展示。
"""


class NewsAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = [
        # "docid",
        # "url",
        # "wapurl",
        "title",
        "intro",
        # "img",
        # "images",
        "keywords",
        "media_name",
        "subject",
        # "text",
        # "html",
        "intime",
        "view_count",
    ]
    # 需要过滤字段
    list_filter = [
        "media_name",
        "subject",
        "view_count",
    ]
    # 需要搜索字段
    list_search = [
        "title",
        "intro",
        "keywords",
        "media_name",
        "subject",
    ]
    list_per_page = 10
    list_max_show_all = 200
    # 发布时间倒序
    ordering = ['-intime']


admin.site.register(News, NewsAdmin)

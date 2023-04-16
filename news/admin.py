from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
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
    list_filter = [
        "media_name",
        "subject",
        "view_count",
    ]
    list_search = [
        "title",
        "intro",
        "keywords",
        "media_name",
        "subject",
    ]
    list_per_page = 10
    list_max_show_all = 200


admin.site.register(News, NewsAdmin)

from django.urls import path
from .views import *

urlpatterns = [
    path("news/", get_list),  # 列表的路由地址
    path("news/detail/", get_detail),  # 详情的路由地址
    path("pie/", pie),  # 情感分析饼图
    path("sentiment/", sentiment),  # 情感分析
    path("keywords/", keywords),  # 关键词分析
    path("tag/", tag),  # 词性分析
    path("summary/", summary),  # 摘要分析
]

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

# useful for handling different item types with a single interface
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_analysis_system.settings")
django.setup()

"""存储数据到数据库中"""


class SpiderPipeline:
    def process_item(self, item, spider):
        from news.models import News

        try:
            n = News.objects.create(**item)
            spider.log(f'{n.title}, {n.intro}')
        except:
            pass
        return None

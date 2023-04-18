import json
from datetime import datetime
from random import random

import scrapy


# 爬虫入口 执行scrapy crawl sina
def get_attrs(d, *fields):
    return {k: v for k, v in d.items() if k in fields}


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = []
    start_urls = []
    channels = {
        # "2509": "全部",
        # "2510": "国内",
        # "2511": "国际",
        "2669": "社会",
        # "2512": "体育",
        # "2513": "娱乐",
        # "2514": "军事",
        # "2515": "科技",
        # "2516": "财经",
        # "2517": "股市",
        # "2518": "美股",
        # "2968": "国内_国际",
        # "2970": "国内_社会",
        # "2972": "国际_社会",
        # "2974": "国内国际社会"
    }

    api = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={lid}&k=&num=50&page={page}&r={r}"

    def start_requests(self):
        # 爬取五十页新闻 新浪只提供50页
        page_total = 50
        for lid, subject in self.channels.items():
            r = random()
            for page in range(1, page_total + 1):
                url = self.api.format(lid=lid, page=page, r=r)
                yield scrapy.Request(url, meta=dict(page=page, lid=lid, subject=subject))

    def parse(self, response, *args, **kwargs):
        meta = response.meta
        try:
            result = json.loads(response.text)["result"]
        except Exception as error:
            print(error, 'error')
            print('-' * 20)
            pass
        else:
            # start_ts = result["start"]
            # if datetime.fromtimestamp(start_ts).strftime(
            #         "%Y-%m-%d"
            # ) == datetime.now().strftime("%Y-%m-%d"):
            # 列表
            for item in result["data"]:
                meta["item"] = item
                yield scrapy.Request(
                    item["url"], meta=meta, callback=self.parse_page
                )
            # # 翻页
            # page = meta["page"] + 1
            # lid = meta["lid"]
            # url = self.api.format(lid=lid, page=page)
            # print(url, 'urlllllllllllll')
            # yield scrapy.Request(url)

    @staticmethod
    def parse_page(response):
        meta = response.meta
        data = meta["item"]
        text = ""
        html = ""
        for el in response.css(
                "#article,#artibody > *:not(.wap_special):not(script):not(#left_hzh_ad):not(style)"
        ):
            text += el.xpath("string(.)").extract_first() + "\n"
            html += el.extract() + "\n"
        item = get_attrs(
            data,
            "title",
            "url",
            "keywords",
            "intro",
            "media_name",
            "docid",
            "wapurl",
            "images",
            "img",
        )
        item["img"] = json.dumps(item["img"], ensure_ascii=False)
        item["images"] = json.dumps(item["images"], ensure_ascii=False)
        item["subject"] = meta["subject"]
        item["text"] = text
        item["html"] = html
        item["intime"] = datetime.fromtimestamp(int(data["intime"])).strftime(
            "%Y-%m-%d"
        )
        if item["media_name"] != "新浪彩票":
            yield item

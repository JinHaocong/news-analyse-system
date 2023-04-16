# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
from datetime import datetime, timedelta
from hashlib import md5

from scrapy import signals, Item, Request
from scrapy.utils.url import urlparse


class IPPoolDownloaderMiddleWare(object):
    """
    代理池中间件
    必须配合HttpProxyMiddleWare使用, 并且要在其之前
    """

    def __init__(self, host, port, order_no, secret, domains=[]):
        self.host = host
        self.port = port
        self.host_port = '%s:%s' % (host, port)
        self.order_no = order_no
        self.secret = secret
        # 需要做ip池代理的域名
        self.ip_pool_domains = domains

    @classmethod
    def from_crawler(cls, crawler):
        # ip池URL
        host = crawler.settings.get('IP_POOL_HOST')
        port = crawler.settings.get('IP_POOL_PORT')
        order_no = crawler.settings.get('IP_POOL_ORDER_NO')
        secret = crawler.settings.get('IP_POOL_SECRET')
        domains = crawler.settings.get('IP_POOL_DOMAINS', [])[0:]
        cls.enable_ip_proxy_to_all_spider = crawler.settings.get(
            'ENABLE_IP_PROXY_TO_ALL_SPIDER', False)
        return cls(host=host, port=port, order_no=order_no, secret=secret, domains=domains)

    def process_request(self, request, spider):
        if not request.meta.get('noproxy', False):
            self._set_ip_pool(request)

    def _set_ip_pool(self, request):
        """
        配置ip池代理
        :param request:
        :return:
        """
        url = self._get_real_url(request)
        scheme = urlparse(url).scheme
        proxy_url = '%s://%s' % (scheme, self.host_port)

        if 'splash' in request.meta:
            splash_args = request.meta['splash']['args']
            splash_args['proxy'] = 'http://%s' % self.host_port
            splash_args['proxy_info'] = dict(
                host=self.host, port=self.port, scheme=scheme)
            # 这里需要清除 proxy meta(该meta有可能来源于上层请求), 否则访问splash的请求也会走代理, 然而我们希望的是splash通过代理访问目标地址
            if 'proxy' in request.meta:
                del request.meta['proxy']
        else:
            request.meta['proxy'] = proxy_url

        timestamp = int(time.time())
        sign_text = 'orderno=%(order_no)s,secret=%(secret)s,timestamp=%(timestamp)s' % dict(order_no=self.order_no,
                                                                                            secret=self.secret,
                                                                                            timestamp=timestamp)
        sign = md5(sign_text.encode('utf-8')).hexdigest().upper()
        auth = 'sign=%(sign)s&orderno=%(order_no)s&timestamp=%(timestamp)s' % dict(sign=sign, order_no=self.order_no,
                                                                                   timestamp=timestamp)
        request.headers['Proxy-Authorization'] = auth

    def _get_real_url(self, request):
        """
        获取实际要请求的url(与splash兼容)
        :param request:
        :return:
        """
        meta = request.meta or {}
        is_splash = 'splash' in meta
        return meta.get('splash').get('args').get('url') if is_splash else request.url

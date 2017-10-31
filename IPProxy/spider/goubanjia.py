#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import datetime
from lxml import etree

import requests
import time

from parsel import Selector


class GouBanJia(object):
    def __init__(self):
        self.url='http://www.goubanjia.com/free/gngn/index{page}.shtml'
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0,'
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36,'
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0,'
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1,'
        ]
    def get_url(self,url):
        for tries in range(5):
            try:
                content = requests.get(url, headers={'User-Agent': random.choice(self.user_agent)}, timeout=30).content
                #                 content = requests.post(url, data=parse.urlencode(data).encode("utf8"), timeout=30).text
                return content
            except:
                if tries < (5 - 1):
                    time.sleep(tries + 1)  # hava a rest
                    print('retry:' + url)
                    continue
                else:
                    print('did not get data')
                    return ''
    def get_proxy(self,html):
        html = etree.HTML(html)
        all_proxy = html.xpath('//table//tr[td]')
        # print(all_proxy)
        for i in all_proxy:
            ip_port = ''.join(i.xpath('td[1]/span[@style]/text()|'
                                      'td[1]/div[@style]/text()|'
                                      'td[1]/p[@style]/text()|'
                                      'td[1]/text()|'
                                      'td[1]/span[@class]/text()'))
            ip, port = ip_port.split(':')
            anonymous = i.xpath('./td[2]/a/text()')[0]
            http_type = ''.join(i.xpath('./td[3]/a/text()')) or 'http'
            country = ''.join(i.xpath('./td[4]/a/text()'))
            speed=i.xpath('td[6]/text()')[0]
            from_site = 'goubanjia'
            proxy = (ip, port, country, anonymous, http_type, speed, from_site)
            yield proxy
    def start(self):
        for page in range(1, 2):
            url = self.url.format(page=page)
            html = self.get_url(url)
            for proxy in self.get_proxy(html):
                yield proxy

if __name__ == '__main__':
    p = GouBanJia()
    for i in p.start():
        print(i)
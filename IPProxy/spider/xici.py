#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from lxml import etree
from multiprocessing.pool import Pool

import requests
import time
from parsel import Selector

from IPProxy.mysql.mysql import MySql


class XiCiProxy(object):
    def __init__(self):
        self.url='http://www.xicidaili.com/nn/{page}'
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3095.5 Safari/537.36'
        ]
        self.mysql=MySql()
    def get_url(self,url):
        for tries in range(5):
            ip=[]
            port=[]
            false_ip=[]
            ips,ports=self.mysql.check_ip(ip,port)
            num=random.randint(1,len(ips))
            proxies = {
                'https': 'http://{ip}:{port}'.format(ip=ips[num],port=ports[num]),
                'http': 'http://{ip}:{port}'.format(ip=ips[num],port=ports[num])
            }
            print(proxies)
            try:
                start=time.time()
                content = requests.get(url, headers={'User-Agent': random.choice(self.user_agent)},timeout=8)
                #                 content = requests.post(url, data=parse.urlencode(data).encode("utf8"), timeout=30).text
                speed = round(time.time() - start, 2)
                print('网站的相应时间为:',speed)
                return content.text
            except:
                if tries < (5- 1):
                    time.sleep(tries + 1)  # hava a rest
                    print('retry:' + url)
                    continue
                else:
                    print('did not get data')
                    print('删除这个ip',ips[num])
                    # false_ip.append(ips[num])
                    # self.mysql.delete_ip(false_ip)
                    self.get_url(url)
                    # return ''
    def get_proxy(self,html):
        # print(html)
        html = etree.HTML(html)
        table = html.xpath('//table//tr[td]')
        # trs = table.xpath('//tr')[1:]  # 去掉标题行
        # ip_list = []
        for tr in table:
            ip = tr.xpath('td[2]/text()')[0]
            port = tr.xpath('td[3]/text()')[0]
            address = tr.xpath('string(td[4]/a)').strip()
            anonymous = tr.xpath('td[5]/text()')[0]
            http_type = tr.xpath('td[6]/text()')[0]
            speed=tr.xpath('td[7]/div[1]/@title')[0]
            # // *[ @ id = "ip_list"] / tbody / tr[2] / td[7] / div
            source='xicidaili'
            proxy = (ip, port, address, anonymous, http_type, speed, source)
            yield proxy
    def start(self):
        for page in range(1,2):
            url=self.url.format(page=page)
            html=self.get_url(url)
            # print(html)
            for proxy in self.get_proxy(html):
                yield proxy
if __name__ == '__main__':
    p = XiCiProxy()
    for i in p.start():
        print (i)
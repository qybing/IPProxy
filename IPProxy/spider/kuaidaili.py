# coding: utf-8

import time
import random
from datetime import datetime

import requests
from lxml import etree


class KuaiDaiLi(object):
    def __init__(self):
        self.ha_url = 'http://www.kuaidaili.com/free/inha/{page}/'  # 1,2,3
        self.tr_url = 'http://www.kuaidaili.com/free/intr/{page}/'
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0,'
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36,'
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0,'
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1,'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3095.5 Safari/537.36'
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
    def get_proxy(self, html):
        html = etree.HTML(html)
        print(html)
        all_proxy = html.xpath('//table//tr[td]')
        for i in all_proxy:
            ip = i.xpath('./td[1]/text()')[0]
            port = i.xpath('./td[2]/text()')[0]
            http_type = i.xpath('./td[4]/text()')[0]
            country = i.xpath('./td[5]/text()')[0]
            speed=i.xpath('td[6]/text()')[0]
            anonymous = i.xpath('./td[3]/text()')[0]
            from_site = 'kuaidaili'
            # crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            proxy = (ip, port, country, anonymous, http_type, speed, from_site)
            yield proxy

    def start(self):
        # for page in range(1, 2):
        #     ha_url = self.ha_url.format(page=page)
        #     time.sleep(1)
        #     for proxy in self.get_proxy(url=ha_url):
        #         yield proxy
        for page in range(1,2):
            url = self.ha_url.format(page=page)
            html = self.get_url(url)
            for proxy in self.get_proxy(html):
                yield proxy


if __name__ == '__main__':
    p = KuaiDaiLi()
    for p_ip in p.start():
        print(p_ip)

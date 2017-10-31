#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from concurrent import futures
from multiprocessing.dummy import Pool

import requests
import time

from IPProxy.mysql.mysql import MySql
from IPProxy.spider.goubanjia import GouBanJia
from IPProxy.spider.ip181 import Ip181Proxy
from IPProxy.spider.ip_chi import IpchiProxy
from IPProxy.spider.kuaidaili import KuaiDaiLi
from IPProxy.spider.xici import XiCiProxy
class Validator(object):
    def __init__(self):
        self.url='http://1212.ip138.com/ic.asp'
        self.ip_list = []
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) '
            'Chrome/24.0.1292.0 Safari/537.14,'
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0,'
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/41.0.2225.0 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36,'
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/27.0.1453.116 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/29.0.1547.62 Safari/537.36,'
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0,'
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36,'
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1,'
        ]
        self.false_ip = []
        self.time=[]
        self.xici=XiCiProxy()
        self.goubanjia=GouBanJia()
        self.kuaidaili=KuaiDaiLi()
        self.ip_chi=IpchiProxy()
        self.ip181=Ip181Proxy()
        self.mysql=MySql()
    def get_proxy(self):
        # for proxy in self.kuaidaili.start():
        #        self.ip_list.append(proxy)
        # for proxy in self.xici.start():
        #        self.ip_list.append(proxy)
        # for proxy in self.goubanjia.start():
        #        self.ip_list.append(proxy)
        # for proxy in self.ip_chi.start():
        #        self.ip_list.append(proxy)
        for proxy in self.ip181.start():
               self.ip_list.append(proxy)
        return self.ip_list
    def check_proy(self,proxy):
        proxies = {
            'https': 'http://{ip}:{port}'.format(ip=proxy[0], port=proxy[1]),
            'http': 'http://{ip}:{port}'.format(ip=proxy[0], port=proxy[1])
        }
        try:
            res = requests.get(self.url, proxies=proxies, headers={'User-Agent': random.choice(self.user_agent)}, timeout=5)
            if res.status_code == 200:
                print('ip可用：', proxy[4]+'://'+proxy[0]+':'+proxy[1])
                # print(res.text)
                return  proxy
            else:
                res.raise_for_status()  # 如果响应状态码不是200,主动抛出异常
        except requests.RequestException as e:
            print("验证代理IP"+ "时发生如下错误")
            print(e)
    def start(self):
        # with futures.ThreadPoolExecutor(max_workers=20) as executor:
        #     future = executor.submit(self.get_proxy)
        #     ip_list=future.result()
        ip_list=self.get_proxy()
        use_ip=[]
        pool=Pool(100)
        ip_pool=pool.map(self.check_proy,ip_list)
        use_ip=([str for str in ip_pool if str not in [None]])
        self.mysql.insert_proxy_to_mysql(use_ip)
        pool.close()
        return
    def test_ip(self,ip,port,q,w):
        proxies = {
            'https': 'http://{ip}:{port}'.format(ip=ip, port=port),
            'http': 'http://{ip}:{port}'.format(ip=ip, port=port)
        }
        for tries in range(3):
                try:
                    start = time.time()
                    res = requests.get(self.url, proxies=proxies, headers={'User-Agent': random.choice(self.user_agent)},
                                       timeout=7)
                    if res.status_code == 200:
                        a=[]
                        speed = round(time.time() - start, 2)
                        print('ip可用：',str(ip) + ':' + str(port))
                        a.append(ip)
                        a.append(str(speed))
                        w.put(a)
                        # self.mysql.up_speed(speed,ip)
                    else:
                        res.raise_for_status()# 如果响应状态码不是200,主动抛出异常
                        q.put(ip)
                        # false_ip.append(ip)
                        # self.mysql.delete_ip(ip)
                except requests.RequestException as e:
                    if tries < (3 - 1):
                        time.sleep(tries + 1)  # have a rest
                        print('重新请求')
                        continue
                    else:
                        print("验证代理IP" + "时发生如下错误")
                        print(e)
                        q.put(ip)
        while not q.empty():
            self.false_ip.append(q.get())
        while not w.empty():
            self.time.append(w.get())
        # print(self.false_ip)
                        # false_ip.append(ip)
        # print('共删除了%s个不可用的ip' % (len(false_ip)))
        # time.sleep(2)
        # self.mysql.delete_ip(self.false_ip)
if __name__=='__main__':
    validator=Validator()
    validator.start()
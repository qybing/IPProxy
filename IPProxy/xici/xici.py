#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from lxml import etree
from multiprocessing import Pool
import requests
from parsel import Selector
def get_result_from_url(url):
    # try 5 times to get result
    header={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,image/apng, */*;q=0.8',
    'Accept - Encoding':'gzip,deflate',
    'Accept - Language':'zh-CN,zh;q = 0.8',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3095.5 Safari/537.36"
    }
    for tries in range(5):
        try:
            content = requests.get(url, headers=header, timeout=30).text
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
def parse(html):
    selector = Selector(text=html)
    table = selector.xpath('//table[@id="ip_list"]')[0]
    trs = table.xpath('//tr')[1:]  # 去掉标题行
    ip_list=[]
    for tr in trs:
        ip = tr.xpath('td[2]/text()').extract()[0]
        port=tr.xpath('td[3]/text()').extract()[0]
        position = tr.xpath('string(td[4])').extract()[0].strip()
        type = tr.xpath('td[6]/text()').extract()[0]
        speed = tr.xpath('td[7]/div/@title').re('\d+\.\d*')[0]
        last_check_time = tr.xpath('td[10]/text()').extract()[0]
        ip_list.append(str(ip)+':'+str(port))
    return ip_list
def check_ip(ip):
    tar_url = "http://ip.chinaz.com/getip.aspx"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3095.5 Safari/537.36"
    }
    proxies = {
        "http": ip,
    }
    try:
        res = requests.get(tar_url, proxies=proxies, headers=headers, timeout=5)
        if res.status_code == 200:
            print('ip可用：',ip)
            return ip
        else:
            res.raise_for_status()  # 如果响应状态码不是200,主动抛出异常
    except requests.RequestException as e:
        print("验证代理IP" + ip + "时发生如下错误 :")
        print(e)
    pass
def main():
    url='http://www.xicidaili.com/nn/'+str(1)
    html=get_result_from_url(url)
    # print(html)
    ip_list=parse(html)
    threads = []
    for i in range(len(ip_list)):
        thread = threading.Thread(target=check_ip,args=(ip_list[i],))
        # print(thread)
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

if __name__=='__main__':
    main()
    pool = Pool()
    pool.map(main,[i for i in range(1,2)])
    pool.close()
    pool.join()
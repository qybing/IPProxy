#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
# import concurrent.futures
from queue import Queue

import pymysql
import re

import time
from queue import Queue
from IPProxy.mysql.mysql import MySql
from IPProxy.validator.Validator import Validator
class Scheduler(object):
    def __init__(self):
        self.q=Queue()
        self.w= Queue()
        self.valiadator=Validator()
        self.mysql=MySql()
    def check_ip_num(self):
        ip=[]
        port=[]
        ip_num=self.mysql.check_ip_num()
        ip,port=self.mysql.check_ip(ip,port)
        threads = []
        for i in range(len(ip)):
            thread = threading.Thread(target=self.valiadator.test_ip, args=(ip[i],port[i],self.q,self.w))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print('这是最后吗')
        # print(self.valiadator.false_ip)
        self.mysql.delete_ip(self.valiadator.false_ip)
        print('删除成功')
        print('时间',self.valiadator.time)
        print(len(self.valiadator.time))
        print(self.valiadator.time[0][0])
        print(self.valiadator.time[0][1])
        self.mysql.up_speed(self.valiadator.time)
        # if int(ip_num[0])<100:
        #     print('ip不足，开始抓取')
        #     self.valiadator.start()
if __name__=='__main__':
    sche=Scheduler()
    sche.check_ip_num()
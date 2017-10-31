#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import re


class MySql(object):
    def __init__(self):
        # self.db = pymysql.connect(host='114.215.99.152', user='dbadmin', passwd='Ic-admin-152', db='test',
        #                           charset='utf8')
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='test',
                                  charset='utf8')
        self.cursor = self.db.cursor()
        # self.db.ping()
    def __del__(self):
        self.cursor.close()
        self.db.close()
        # print("finish")
    def insert_proxy_to_mysql(self,proxy):
        print(len(proxy))
        print(proxy)
        for i in range(len(proxy)):
            sql="replace into pool(ip,port,address,anonymous,http_type,speed,source) values(%s,%s,%s,%s,%s,%s,%s)"
            try:
                self.cursor.execute(sql,(proxy[i][0],proxy[i][1],proxy[i][2],proxy[i][3],proxy[i][4],proxy[i][5],proxy[i][6]))
                self.db.commit()
            except Exception as e:
                print(e)
        return True
    def check_ip_num(self):
        sql = "select count(ip) from pool"
        self.cursor.execute(sql)
        ip_num = str(self.cursor.fetchone())
        number = re.compile(r'\d+')
        return number.findall(ip_num)
    def check_ip(self,ip,port):
        sql='select ip,port from pool order by speed'
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        for row in rs:
            ip.append(row[0])
            port.append(row[1])
        return ip,port
    def delete_ip(self,false_ip):

        for i in range(len(false_ip)):
            sql="delete from pool where ip='%s'"%(false_ip[i])
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                raise e
    def up_speed(self,speed):
        for i in range(len(speed)):

            sql="update pool set speed='%s' where ip='%s'"%(speed[i][1],speed[i][0])
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                raise e
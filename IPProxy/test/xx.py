#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import time

import chardet

a=random.randint(1,9)
print(a)
import requests
r = requests.get("http://www.baidu.com")
r.encoding = chardet.detect(r.content)['encoding']
if r.ok:
    print(r.ok)
    c=r.elapsed.microseconds
    print(c/1000000)
    start=time.time()
    time.sleep(1)
    e=time.time()
    speed = round(time.time() - start, 2)
    print(speed)
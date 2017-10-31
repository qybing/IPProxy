#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
f = open('hello.html', 'r',encoding='utf-8')
html = f.read()
f.close()
print(html)
selector = etree.HTML(html)
content = selector.xpath('//ul[@id="useful"]/li/text()')
for each in content:
    print (each)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue
from queue import Queue
a=[[1,2,3],[2]]
q = Queue()
for i in range(5):
    q.put(i)

while not q.empty():
    print (q.get())
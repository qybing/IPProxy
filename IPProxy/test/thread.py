#!/usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue
import sys
import Queue
import threading
from queue import Queue
q = Queue.Queue()
def worker1(x, y):
    func_name = sys._getframe().f_code.co_name
    print ("%s run ..." % func_name)
    q.put((x + y, func_name))
def worker2(x, y):
    func_name = sys._getframe().f_code.co_name
    print("%s run ..." % func_name)
    q.put((x - y, func_name))
if __name__ == '__main__':
    result = list()
    t1 = threading.Thread(target=worker1, name='thread1', args=(10, 5, ))
    t2 = threading.Thread(target=worker2, name='thread2', args=(20, 1, ))
    print ('-' * 50)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    while not q.empty():
        result.append(q.get())
    print(result)
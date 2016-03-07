# -*-coding:utf-8 -*-
# 
# Created on 2016-03-04, by felix
# 

__author__ = 'felix'

import requests
import time
import sys
import threading

from Queue import Queue

SLEEP_TIME = 6


class Worker(threading.Thread):
    def __init__(self, work_queue, result_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            func, args = self.work_queue.get()
            res = func(args)
            self.result_queue.put(res)
            if self.result_queue.full():
                res = [self.result_queue.get() for i in range(self.result_queue.qsize())]
                for obj in res:
                    print obj
            self.work_queue.task_done()


class Stock(object):
    """股票实时价格获取"""

    THREAD_NUM = 5

    def __init__(self, code):
        self.code = code
        self.work_queue = Queue()
        self.threads = []
        self.__init_thread_poll(self.THREAD_NUM)

    def __init_thread_poll(self, thread_num):
        self.params = self.code.split(',')
        self.params.extend(['s_sh000001', 's_sz399001'])
        self.result_queue = Queue(maxsize=len(self.params))
        for i in range(thread_num):
            self.threads.append(Worker(self.work_queue, self.result_queue))

    def __add_work(self, stock_code):
        self.work_queue.put((self.value_get, stock_code))

    def del_params(self):
        for obj in self.params:
            self.__add_work(obj)

    def wait_all_complete(self):
        for thread in self.threads:
            if thread.isAlive():
                thread.join()

    @classmethod
    def value_get(cls, code):
        slice_num, value_num = 21, 3
        if code in ['s_sh000001', 's_sz399001']:
            slice_num = 23
            value_num = 1
        r = requests.get("http://hq.sinajs.cn/list=%s" % (code,))
        name, now = r.text.split(',')[0][slice_num:], r.text.split(',')[value_num]
        return name + now


if __name__ == '__main__':
    assert len(sys.argv) > 1, "Please enter the stock code!"  # 是否输入股票代码

    if filter(lambda s: s[:-6] not in ('sh', 'sz', 's_sh', 's_sz'), sys.argv[1].split(',')):  # 股票代码输入是否正确
        raise ValueError

    stock = Stock(sys.argv[1])
    while True:
        stock.del_params()
        time.sleep(SLEEP_TIME)

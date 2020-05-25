# -*-coding:utf-8 -*-
# 
# Created on 2016-03-04, by felix
# 

__author__ = 'felix'

import requests
import time
import sys
import threading

import queue
from optparse import OptionParser


class Worker(threading.Thread):
    """多线程获取"""
    def __init__(self, work_queue, result_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            func, arg, code_index = self.work_queue.get()
            res = func(arg, code_index)
            self.result_queue.put(res)
            if self.result_queue.full():
                res = sorted([self.result_queue.get() for i in range(self.result_queue.qsize())], key=lambda s: s[0], reverse=True)
                res.insert(0, ('0', u'名称     股价	实时涨幅	昨日价格'))
                print ('***** start *****')
                for obj in res:
                    print (obj[1])
                print ('***** end *****\n')
            self.work_queue.task_done()


class Stock(object):
    """股票实时价格获取"""

    def __init__(self, code, thread_num):
        self.code = code
        self.work_queue = queue.Queue()
        self.threads = []
        self.__init_thread_poll(thread_num)

    def __init_thread_poll(self, thread_num):
        self.params = self.code.split(',')
        self.params.extend(['s_sh000001', 's_sz399001'])  # 默认获取沪指、深指
        self.result_queue = queue.Queue(maxsize=len(self.params[::-1]))
        for i in range(thread_num):
            self.threads.append(Worker(self.work_queue, self.result_queue))

    def __add_work(self, stock_code, code_index):
        self.work_queue.put((self.value_get, stock_code, code_index))

    def del_params(self):
        for obj in self.params:
            self.__add_work(obj, self.params.index(obj))

    def wait_all_complete(self):
        for thread in self.threads:
            if thread.isAlive():
                thread.join()

    @classmethod
    def value_get(cls, code, code_index):
        slice_num, value_num,begin_num = 21, 3 ,2
        name, now  = u'——无——', u'  ——无——'
        if code in ['s_sh000001', 's_sz399001']:
            slice_num = 23
            value_num = 1
            begin_num = 3
        r = requests.get("http://hq.sinajs.cn/list=%s" % (code,))
        res = r.text.split(',')
        if len(res) > 1:
            name, now, begin = r.text.split(',')[0][slice_num:], r.text.split(',')[value_num],float(r.text.split(',')[begin_num])
        if code in ['s_sh000001', 's_sz399001']:
            rate = begin
            begin = float(now)/(1 + (begin)/100)
        else:
            rate = (float(now) - (begin))/(begin) *100
        if(rate >1 or rate < -1):
            print("*******" + name + "**********")
        return code_index, name + ' ' + now + ' ' + str(round(rate,3)) + ' ' + str(round(begin,3))


if __name__ == '__main__':
    parser = OptionParser(description="Query the stock's value.", usage="%prog [-c] [-s] [-t]", version="%prog 1.0")
    parser.add_option('-c', '--stock-code', dest='codes',
                      help="the stock's code that you want to query.")
    parser.add_option('-s', '--sleep-time', dest='sleep_time', default=6, type="int",
                      help='How long does it take to check one more time.')
    parser.add_option('-t', '--thread-num', dest='thread_num', default=3, type='int',
                      help="thread num.")
    options, args = parser.parse_args(args=sys.argv[1:])

    assert options.codes, "Please enter the stock code!"  # 是否输入股票代码
    aa =filter(lambda s: s[:-6] not in ('sh','f_' ,'sz', 's_sh', 's_sz'), options.codes.split(','))
    if aa:
        print(aa)
    if list(aa):
        print(list(aa))
    print(aa)
    for a in aa:
        if a[:-6] not in ('sh', 'sz','s_sh'):
            print(a[:-6])
    if list(filter(lambda s: s[:-6] not in ('sh','f_' ,'sz', 's_sh', 's_sz'), options.codes.split(','))):  # 股票代码输入是否正确
        raise ValueError

    stock = Stock(options.codes, options.thread_num)

    while True:
        stock.del_params()
        time.sleep(options.sleep_time)

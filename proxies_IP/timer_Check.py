'''
    IP池定时维护
'''
import threading
from queue import Queue

import db_Handler
from check_IP import IP_Checker
import get_IP
import run


def supplement():
    # 从网页获取的未验证IP存储
    IP_Q = Queue()
    # 子线程：从代理网页获取代理
    IP_Acq = get_IP.IP_Acquirer(IP_Q)
    IP_Acq.start()
    # 子线程：可用代理检测 
    checkers = list()
    for i in range(run.checkProcess_Num):
        checker = IP_Checker(IP_Q, IP_Acq)
        checker.start()
        checkers.append(checker)
    for i in checkers:
        i.join()


useless_IP = 0


def thread_Check(IP_Q):
    global useless_IP
    while not IP_Q.empty():
        temp = IP_Q.get()
        if not IP_Checker.IP_Check(temp[0]):
            db_Handler.db_Delete(temp[0])
            useless_IP += 1


def timer_Checker():
    IP_Q = Queue()
    proxies = db_Handler.db_GetAll()
    global useless_IP
    useless_IP = 0
    print("------IP池定时维护开始工作------")
    for _ in proxies:
        IP_Q.put(_)
    checkers = list()
    for i in range(run.maintainProcess_Num):
        checker = threading.Thread(target=thread_Check, args=(IP_Q, ))
        checker.start()
        checkers.append(checker)
    for item in checkers:
        item.join()
    usable = len(proxies) - useless_IP
    print('检测IP:%d 个,剔除IP:%d个,有效IP:%d个' % (len(proxies), useless_IP, usable))
    print("------IP池定时维护工作结束------")
    if usable < run.least_IP:
        print("--有效IP量过低,开始补充IP--")
        supplement()
        print("---------IP补充完毕--------")
    run.timer = threading.Timer(60 * run.check_Period, timer_Checker)
    run.timer.start()


if __name__ == '__main__':
    timer_Checker()


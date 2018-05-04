'''
    IP有效性检测
'''
from threading import Thread
import requests

import run
import db_Handler


class IP_Checker(Thread):
    def __init__(self, IP_Q, thread_Temp):
        super(IP_Checker, self).__init__()
        self.conn, self.db_Cur = db_Handler.db_Connect()
        self.IP_Q = IP_Q
        self.thread_Temp = thread_Temp

    def run(self):
        while not (self.IP_Q.empty() and not self.thread_Temp.isAlive()):
            if db_Handler.db_RowNum() >= run.full_IP:
                break
            proxies = self.IP_Q.get()
            if self.IP_Check(proxies[0]):
                if db_Handler.db_RowNum() >= run.full_IP:
                    break
                db_Handler.db_Put(self.conn, self.db_Cur, proxies)
        self.db_Cur.close()
        self.conn.close()

    @staticmethod
    def IP_Check(IP_ForChecking):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.7\
            5 Safari/537.36'}
        url = 'http://httpbin.org/ip'
        url = 'http://www.baidu.com'
        prox = {"http": 'http:' + IP_ForChecking}
        try:
            res = requests.get(url, headers=headers, proxies=prox, timeout=4)
        except Exception as e:
            try:
                res = requests.get(url, headers=headers, proxies=prox, timeout=4)
            except Exception as e:
                print(IP_ForChecking, 'is useless')
                return False
            else:
                if res.status_code == 200:
                    print(IP_ForChecking, 'is OK')
                    return True
        else:
            if res.status_code == 200:
                print(IP_ForChecking, 'is OK')
                return True




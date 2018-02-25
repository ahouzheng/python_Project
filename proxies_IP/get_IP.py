'''
    从代理源获取IP
'''
import requests
from bs4 import BeautifulSoup as BS
import time
import re
from threading import Thread
from queue import Queue


class IP_Acquirer(Thread):

    def __init__(self, IP_Q):
        super(IP_Acquirer, self).__init__()
        self.IP_Q = IP_Q
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.7\
            5 Safari/537.36'}
        self.IP_Sources = [self.IP_Source1, self.IP_Source2, self.IP_Source3, self.IP_Source4, self.IP_Source5]
        
    def run(self):   
        for item in self.IP_Sources:
            pro = item()     
            for _ in pro:
                self.IP_Q.put(_)

    def IP_Get(self):
        pass

    def IP_Source1(self):
        '''
        IP代理源：西刺代理 http://www.xicidaili.com
            每页100个
        '''
        urls = ['http://www.xicidaili.com/nn',  # 高匿
                'http://www.xicidaili.com/nt']  # 透明
        for _ in urls:
            try:
                res = requests.get(_, headers=self.headers)
                soup = BS(res.text, 'html.parser')
                proxies = soup.find_all(id='ip_list')[0].find_all('tr')[1:]
            except Exception as e:
                print('source1', e.args)
                return
            for _ in proxies:
                proxie = _.find_all('td')
                proxie = ':'.join((proxie[1].text, proxie[2].text)), proxie[4].text
                yield proxie

    def IP_Source2(self):
        '''
        IP代理源：快代理  https://www.kuaidaili.com
            每页15 个
        '''
        urls = ['https://www.kuaidaili.com/free/inha/',  # 高匿
                'https://www.kuaidaili.com/free/intr/']  # 透明
        for _ in urls:
            try:
                res = requests.get(_, headers=self.headers)
                soup = BS(res.text, 'html.parser')
                proxies = soup.find_all(id='list')[0].find_all('tbody')[0].find_all('tr')
            except Exception as e:
                print('source2', e.args)
                return
            for __ in proxies:
                proxie = __.find_all('td')[0:3]
                yield ':'.join((proxie[0].text, proxie[1].text)), proxie[2].text.replace('高匿名', '高匿')
            time.sleep(1)  # 该网站过快访问返回 '-10'

    def IP_Source3(self):
        '''
        IP代理源：66代理 http://www.66ip.cn
            每页量可选
        '''
        urls = ['http://www.66ip.cn/nmtq.php?getnum={getnum}&\
                 isp=0&anonymoustype=3&start=&ports=&export=&\
                 ipaddress=&area=1&proxytype=2&api=66ip',       # 高匿
                'http://www.66ip.cn/nmtq.php?getnum={getnum}&\
                 isp=0&anonymoustype=1&start=&ports=&export=&\
                 ipaddress=&area=1&proxytype=2&api=66ip']       # 透明
        for _ in urls:
            try:
                res = requests.get(_.format(getnum=50), headers=self.headers)
                rp = re.compile(r'[\r\n]|[\t]|["  "]')
                proxies = re.findall(r'src="//static.mediav.com/js/mvf_g2.js"></script>(.*?)</div>', res.text, re.S)[0]
                proxies = rp.sub('', proxies).split(r'<br/>')[0:-1]
            except Exception as e:
                print('source3', e.args)
                return
            for __ in proxies:
                if 'nonymoustype=3' in res.url:
                    __ = __, '高匿'
                if 'nonymoustype=1' in res.url:
                    __ = __, '透明'                    
                yield __

    def IP_Source4(self):
        '''
        IP代理源：云代理 http://www.ip3366.net
            每页15个
        '''
        urls = ['http://www.ip3366.net/free/?stype=1',  # 高匿
                'http://www.ip3366.net/free/?stype=2']  # 透明
        for _ in urls:
            try:
                res = requests.get(_, headers=self.headers)
                soup = BS(res.text, 'html.parser')
                proxies = soup.find_all(id='list')[0].find_all('tbody')[0].find_all('tr')
            except Exception as e:
                print('source4', e.args)
                return
            for _ in proxies:
                proxie = _.find_all('td')[0:3]
                proxie = ':'.join((proxie[0].text, proxie[1].text))
                if 'type=1' in res.url:
                    proxie = proxie, '高匿'
                if 'type=2' in res.url:
                    proxie = proxie, '透明'
                yield proxie

    def IP_Source5(self):
        '''
        IP代理源：无忧代理 http://www.data5u.com
            每页15个
        '''
        urls = ['http://www.data5u.com/free/gngn/index.shtml',  # 高匿
                'http://www.data5u.com/free/gnpt/index.shtml']  # 透明
        for _ in urls:
            try:
                res = requests.get(_, headers=self.headers)
                soup = BS(res.text, 'html.parser')
                proxies = soup.find_all(class_='wlist')[1].find_all('li')[1].find_all('ul')[1:]
            except Exception as e:
                print("source5", e.args)
                return
            for __ in proxies:
                proxie = __.find_all('span')[0:3]
                proxie = proxie[0].text + ':' + proxie[1].text, proxie[2].text
                yield proxie

    def IP_Source6(self):
        '''
        IP代理源：全网代理IP http://www.goubanjia.com
        '''
        urls = ['http://www.goubanjia.com/free/gngn/index.shtml',
                'http://www.goubanjia.com/free/gnpt/index.shtml']
        for _ in urls:
            try:
                res = requests.get(_, headers=self.headers)
                soup = BS(res.text, 'html.parser')
                proxies = soup.find_all(id='list')[0].find_all('tbody')[0].find_all('tr')
            except Exception as e:
                print('source6', e.args)
                return
            for __ in proxies:
                proxie = __.find_all('td')[0:2]
                temp = proxie[0].find_all(('span', 'div'))
                temp = ''.join([x.text for x in temp])
                yield temp

    def IP_Source7(self):
        '''
        IP代理源：181  http://www.ip181.com/
        '''
        url = ['http://www.ip181.com/']

    def IP_Source8(self):
        '''
        IP代理源：讯代理 http://www.xdaili.cn
        '''
        url = ['http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10']


if __name__ == '__main__':
    IP_Q = Queue()
    IP_Acq = IP_Acquirer(IP_Q)
    IP_Acq.start()
    while not (IP_Q.empty() and not IP_Acq.is_alive()):
        print(IP_Q.get())


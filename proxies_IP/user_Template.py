import requests
'''
代理IP池用户接口
此接口运行需提前运行IP池服务
'''


def API_GetOne():
    url = 'http://localhost:5000/get_one/'
    try:
        res = requests.get(url)
        return res.text
    except:
        return 0


def API_GetCount():
    url = 'http://localhost:5000/count/'
    try:
        res = requests.get(url)
        return res.text
    except:
        return 0
    

def API_Delete(proxy):
    # url = 'http://localhost:5000/delete/?ip={}'.format('122.7.122.124:8118')
    url = 'http://localhost:5000/delete/?ip={}'.format(proxy)
    res = requests.get(url=url)
    print(res.text)



if __name__ == '__main__':
    proxy = API_GetOne()
    print(proxy)


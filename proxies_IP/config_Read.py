'''
    获取配置文件信息
'''
from configparser import ConfigParser


def read_Config():
    path = 'config.ini'
    cp = ConfigParser()
    cp.read(path)
    config = {}
    config['full_IP'] = int(cp.get('check_Para', 'full_IP'))
    config['least_IP'] = int(cp.get('check_Para', 'least_IP'))
    config['check_Period'] = int(cp.get('check_Para', 'check_Period'))
    config['checkProcess_Num'] = int(cp.get('process_Num', 'checkProcess_Num'))
    config['maintainProcess_Num'] = int(cp.get('process_Num', 'maintainProcess_Num'))
    return config


if __name__ == '__main__':
    config = read_Config()
    print(config)


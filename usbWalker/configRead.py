'''
    获取配置文件信息
'''
from configparser import ConfigParser


def read_Config():
    path = 'config.ini'
    cp = ConfigParser()
    cp.read(path)
    config = {}
    config['from'] = cp.get('path', 'from')
    config['saveTo'] = cp.get('path', 'saveTo')
    config['getAll'] = cp.get('selectPara', 'getAll')
    if config['getAll'] == 'False':
        config['getAll'] = False
    if config['getAll'] == 'True':
        config['getAll'] = True    
    config['size_Thr'] = int(cp.get('selectPara', 'size_Thr'))
    config['word'] = cp.get('selectPara', 'word').split(',')
    return config


if __name__ == '__main__':
    config = read_Config()
    print(config)

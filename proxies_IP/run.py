import threading
from multiprocessing import Process

import timer_Check
from API_IP import API_Run
import config_Read

config = config_Read.read_Config()
full_IP = config['full_IP']
least_IP = config['least_IP']
check_Period = config['check_Period']
#  IP有效性检测线程数
checkProcess_Num = config['checkProcess_Num']
#  IP池维护检测线程数
maintainProcess_Num = config['maintainProcess_Num']

if __name__ == '__main__':
    timer = threading.Timer(2, timer_Check.timer_Checker)
    timer.start()
    
    pc = Process(target=API_Run)
    pc.start()

    pc.join()

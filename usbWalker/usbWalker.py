import os
import time 
import shutil
import configRead


# 判断文件是否需要复制
def value(file):
    file_Type = file.split('.')[-1].lower()
    if os.path.isfile(file) is False:
        return 0
    if getAll is True:
        return 1
    if file_Type in word:
        return 1
    return 0


#  拷贝文件
def copyfile(root, file):
    file_Path = SAVE + root[3:]
    if not os.path.exists(file_Path):
        os.makedirs(file_Path)
    shutil.copy(os.path.join(root, file), os.path.join(file_Path, file))


#  查看文件大小
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


#  U盘遍历
def usbWalker():
    if not os.path.exists(SAVE): 
        os.mkdir(SAVE)
    print("开始抓取U盘")
    f = open(SAVE + time.strftime("%m%d%H%M", time.localtime(time.time())) + ".txt", "w")
    for root, dirs, files in os.walk(USB): 
        for file in files:
            export = os.path.join(root, file)
            file_Size = get_FileSize(export)
            f.writelines(export + '--' + str(file_Size) + 'MB' + '\n')
            try:
                if file_Size > size_Thr:
                    print('忽略过大文件:' + export)
                elif value(export):
                    print("复制:" + export)
                    copyfile(root, file)
            except Exception as e: 
                print(e)
                print("文件已经忽略")
    f.close
    print("拷贝文件完成")


#  简单判断U盘内容是否变化
def getusb():
    global OLD
    NEW = os.listdir(USB)
    if(len(NEW) == len(OLD)):
        print("U盘内容没有变化")
        return 0
    else:
        OLD = NEW
        return 1


if __name__ == '__main__':
    #  如果存在配置文件则读入
    config = configRead.read_Config()
    USB = config['from']             #u盘目录
    SAVE = config['saveTo']          #保存目录
    getAll = config['getAll']        #为True时拷贝所有文件
    size_Thr = config['size_Thr']    #忽略大于 size_Thr Mb 的文件
    word = config['word']            #要保存的文件后缀列表

    OLD = []
    
    while(1):
        if os.path.exists(USB):
            print("检测到U盘")
            if getusb():
                try:
                    usbWalker()
                    break
                except Exception as e:
                    print("未知错误", e)
        else:
            print("暂时没有U盘")
        time.sleep(10)

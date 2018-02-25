'''
    mysql 数据库相关操作
'''
import pymysql
import random


def db_Connect():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()
    return conn, db_Cur


def db_Create():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()   
    sql_Exe = 'CREATE TABLE IP_Data(\
              IP varchar(25),\
              anonymous text(15))'
    db_Cur.execute(sql_Exe)
    db_Cur.close()
    conn.close()


def db_Clear():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()   
    sql_Exe = 'delete from IP_Data'
    db_Cur.execute(sql_Exe)
    conn.commit()
    db_Cur.close()
    conn.close()


def db_Put(conn, db_Cur, proxies):
    sql_Exe = 'select * from IP_Data where IP="{}"'.format(proxies[0])
    db_Cur.execute(sql_Exe)
    temp = db_Cur.fetchall()
    if len(temp) == 0:
        sql_Exe = "INSERT INTO IP_Data VALUES ('%s', '%s')" % (proxies[0], proxies[1])
        db_Cur.execute(sql_Exe)
        conn.commit()
    else:
        print('IP:%s' % (proxies[0]), '重复,不保存')


def db_RowNum():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()  
    sql_Exe = 'select count(*) from IP_Data'
    db_Cur.execute(sql_Exe)
    row_Num = db_Cur.fetchone()[0]
    db_Cur.close()
    conn.close() 
    return row_Num


def db_GetOne():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()
    sql_Exe = 'select * from IP_Data'
    db_Cur.execute(sql_Exe)
    row = db_Cur.fetchall()
    db_Cur.close()
    conn.close()
    return row[random.randint(0, db_RowNum() - 1)]


def db_GetAll():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()
    sql_Exe = 'select * from IP_Data'
    db_Cur.execute(sql_Exe)
    rows = db_Cur.fetchall()
    db_Cur.close()
    conn.close() 
    return rows


def db_Get():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()
    sql_Exe = 'select * from IP_Data'
    db_Cur.execute(sql_Exe)
    row = db_Cur.fetchone()
    sql_Exe = 'delete from IP_Data where IP = "{}"'.format(row[0])
    db_Cur.execute(sql_Exe)
    conn.commit()
    db_Cur.close()
    conn.close() 
    return row


def db_Delete(proxies):
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()
    sql_Exe = 'delete from IP_Data where IP = "{}"'.format(proxies)
    db_Cur.execute(sql_Exe)
    conn.commit()
    db_Cur.close()
    conn.close() 


def db_Print():
    conn = pymysql.Connect('localhost', 'root', 'kanghua123', 'test', charset='utf8')
    db_Cur = conn.cursor()
    sql_Exe = 'select * from IP_Data'
    db_Cur.execute(sql_Exe)
    rows = db_Cur.fetchall()
    anony_Type1, anony_Type2 = 0, 0
    for _ in rows:
        if '高匿' == _[1]:
            anony_Type1 += 1
        if '透明' == _[1]:
            anony_Type2 += 1
        print(_)
    print('高匿: %d  透明: %d' % (anony_Type1, anony_Type2))
    print("总计: %d 条数据" % db_RowNum())


if __name__ == '__main__':
    db_Print()


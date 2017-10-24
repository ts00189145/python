# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:40:14 2017

@author: IMITA-PC-13
"""

def time():
    now_data = time.strftime("%Y/%m/%d")
    now_time = time.strftime("%H:%M:%S")
    now = now_data + ' ' + now_time
    #取出今天日期、時間，並整成變數now
    


def dbcon():
    import pymysql

    db = pymysql.connect(
    host='localhost',
    port=3306,
    user='testuser',
    passwd='test1234',
    db='testuser',
    charset='utf8'
    )
    '''
    cursor = db.cursor()
    
    db.commit()
    
    db.rollback()
    
    db.close()
    '''
    

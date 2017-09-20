# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:34:05 2017

@author: IMITA-PC-13
"""
#帶入套件
import pymysql.cursors
import pandas as pd
import time

#抓回資料
data = pd.read_csv('http://file.data.gov.tw/event/dataset.csv')

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

#去抓特定欄位
organ = data.T.loc['資料集提供機關']
dataname = data.T.loc['資料集名稱']
browse = data.T.loc['瀏覽次數']
download = data.T.loc['下載次數']
score = data.T.loc['資料集評分']

#連線DB
db = pymysql.connect(
        host='localhost',
        port=3306,
        user='testuser',
        passwd='test1234',
        db='testuser',
        charset='utf8'
    )

cursor = db.cursor()

for i in range(len(data)):
    #print(i)
    #input_to_db(organ,dataname,browse,download,score,i)
    cursor.execute('insert into '+ ' data01 (organ, dataname, browse, download, score, data )' + 
                                             ' values( %s, %s, %s, %s, %s, %s)', 
                   ( 
                    str( organ.iloc[i] ) ,
                    str( dataname.iloc[i] ),
                    str( browse.iloc[i]),
                    str( download.iloc[i]) ,
                    str( score.iloc[i]) ,                    
                    str( now) ) )

try:
    # 執行sql語法
    db.commit()
    # 提交到資料庫執行
    print("成功插入")
    db.close()
except:
    db.rollback()
    print ("MySQL DB Error")
    # 如果有錯誤則回滾
    db.close()
    # 關閉與資料庫的連接


'''
def input_to_db(organ,dataname,browse,download,score,i):

    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='testuser',
        passwd='test1234',
        db='testuser',
        charset='utf8'
    )
    cursor = db.cursor()
    
    cursor.execute('insert into '+ ' data01 (organ, dataname, browse, download, score, data )' + 
                                             ' values( %s, %s, %s, %s, %s, %s)', 
                   ( 
                    str( organ.iloc[i] ) ,
                    str( dataname.iloc[i] ),
                    str( browse.iloc[i]),
                    str( download.iloc[i]) ,
                    str( score.iloc[i]) ,                    
                    str( now) ) )
    try:
        # 執行sql語法
        db.commit()
        # 提交到資料庫執行
        print("成功插入")
        db.close()
    except:
        db.rollback()
        print ("MySQL DB Error")
        # 如果有錯誤則回滾
        db.close()
        # 關閉與資料庫的連接
for i in range(len(data)):
    #print(i)
    input_to_db(organ,dataname,browse,download,score,i)
'''

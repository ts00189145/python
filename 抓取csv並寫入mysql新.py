# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:21:17 2017

@author: IMITA-PC-13
"""
#帶入套件
import pymysql.cursors
import pandas as pd
import time
#連線DB
db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='open_data',
        charset='utf8'
    )
cursor = db.cursor()


#url = 'http://data.tycg.gov.tw/api/v1/rest/datastore/54f0362a-2fac-46ab-9fae-2d9b04958aaa?format=csv'
url = 'http://file.data.gov.tw/event/dataset.csv'
#抓回資料
data = pd.read_csv(url)

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

#資料表名稱 tycg_A（桃園）


#尋找所有的欄位名稱 取出了欄位名稱之後，然後呢？
indexnum = len(data.T.index)
for title in range(0,indexnum):
    print(data.T.index[title])
    #print(data.T.index[title])

dict0 = {}
for titlename in range(0,indexnum):
    print(data.T.index[title])


organ = data.T.loc['資料集提供機關']
dataname = data.T.loc['資料集名稱']
browse = data.T.loc['瀏覽次數']
download = data.T.loc['下載次數']
score = data.T.loc['資料集評分']



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
    
    print('insert into '+ ' data01 (organ, dataname, browse, download, score, data )' + 
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

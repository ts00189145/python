# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:13:33 2017

@author: IMITA-PC-13
"""

#帶入套件
import pymysql.cursors
import pandas as pd
import time
import json
import requests


#讀取資料庫取得設定(這裡先假裝設定是從資料庫讀出來的)
url = 'http://edbkcg.kcg.gov.tw/prices/PricesToJson.php'
tableName = "kcg_A" #資料表名稱

#抓回資料

res = requests.get(url)
a = res.text.encode('ISO-8859-1')
b = a.decode('utf-8-sig')
if b.startswith(u'\ufeff'):
    b = b.encode('utf8')[3:].decode('utf8')
data =  json.loads(b)




#建立資料庫連線
'''
db = pymysql.connect(
    host='192.168.1.74',
    port=3306,
    user='coa',
    passwd='coa',
    db='open_data',
    charset='utf8'
)
'''
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='open_data',
    charset='utf8'
)

cursor = db.cursor()


#建立資料表(先檢查是否已存在)
cursor.execute('SELECT COUNT(*) AS num FROM `information_schema`.`TABLES` WHERE TABLE_NAME="'+tableName+'" AND TABLE_SCHEMA="open_data"')
if cursor.fetchone()[0] == 0:
    createSQL = 'CREATE TABLE IF NOT EXISTS `open_data`.`'+tableName+'` ('+(','.join('`'+data.columns+'` VARCHAR(200)'))+') ENGINE=MYISAM CHARSET=utf8;'
    cursor.execute( createSQL )
else:
    print('資料表"open_data.'+tableName+'"已存在，不用新建')
        
#匯入SQL語法的前半部，這部份大家都一樣
SQL_head = 'insert into '+'`'+tableName+'` ( ' + (','.join('`'+data.columns+'`')) + ' )'\
            +' values('+(' %s,'*len(data.columns))[0:-1] +' )'
#print( 'SQL_head:'+SQL_head+'\n' )


#把所有要執行的SQL語法都放進SQLs裡面
SQLs = list()
SQL_values = list()
for sn in data.index:
    tmp = list()
    for col in data.columns:
        tmp.append( str( data[col][sn] ) )
    SQL_values.append(tuple(tmp))


#所有SQL語法執行一遍
sn = 1
retry = 0 #SQL執行失敗重試次數
retryError = 0 #SQL執行失敗重試後還是失敗次數
totalRow = len(data.index)
for SQL_value in SQL_values:
    try:
        cursor.execute( SQL_head, SQL_value )
    except:
        time.sleep(1)
        retry += 1
        try:
            cursor.execute( SQL_head, SQL_value )
        except:
            retryError += 1
            print(SQL_value)
    if sn%100 == 1:
        print('進度：'+str(sn)+'/'+str(totalRow))
    sn += 1

print('結束，重試'+str(retry)+'次，失敗'+str(retryError)+'次')
#關閉資料庫連結
db.close()


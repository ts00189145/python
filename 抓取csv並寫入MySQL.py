# -*- coding: utf-8 -*-
#帶入套件
from urllib.request import urlopen
from io import StringIO
import csv
import pymysql.cursors
#import pandas as pd
import time

#抓取csv並讀取
url = urlopen('http://file.data.gov.tw/event/dataset.csv').read().decode('utf-8')
datafile = StringIO(url)
csvReader = csv.reader(datafile)

'''
url = pd.read_csv('http://file.data.gov.tw/event/dataset.csv')
url# 這比較好
'''

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

#
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='testuser',
    passwd='test1234',
    db='testuser',
    charset='utf8'
)
#資料庫、使用者、密碼、資料庫

cursor = db.cursor()
#使用cursor()方法获取操作游标 

#這邊要寫迴圈
for row in csvReader:
    #print( type( row[3]  ) )

    
    cursor.execute('insert into '+ 'data01 (organ, dataname, browse, download, score, data)' + ' values( %s, %s, %s, %s, %s, %s)', 
                   ( row[0] , row[1] , row[2] , row[3] , row[4] , now) ) 

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







print('資料抓取日期：' + now)

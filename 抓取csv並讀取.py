# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:19:58 2017

@author: IMITA-PC-13
"""

# -*- coding: utf-8 -*-
import time
#使用時間套件


#正確板（取出單一列資料）
from urllib.request import urlopen
from io import StringIO
import csv
url = urlopen('http://file.data.gov.tw/event/dataset.csv').read().decode('utf-8')
datafile = StringIO(url)
csvReader = csv.reader(datafile)
'''
for row in csvReader:
    print(row[0])
'''
    
import pymysql.cursors

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

#這邊要寫迴圈***這邊有問題
for row in csvReader:
    cursor.execute('insert into '+ 'data01 (organ, dataname, browse, download,score,data)' +' values(%s,%s,%s,%s,%s,%s)', 
                   ( row[0] , row[1] , row[2] , row[3] , row[4] , row[5] , now) ) 



try:
    # 執行sql語法
    db.commit()
    # 提交到資料庫執行
    print("成功插入")
except:
    db.rollback()
    print ("MySQL DB Error")
    # 如果有錯誤則回滾
    db.close()
    # 關閉與資料庫的連接





import csv
import urllib
import requests
#線上下載型
url = 'http://file.data.gov.tw/event/dataset.csv'
response = urllib.request.urlopen(url)#從網路上取得資料
cvsreader = response.read()#讀取cvs檔案
cvsfile = list(cvsreader)#將cvs檔案讀取成list
print(cvsreader.decode('utf-8')) #.encode('utf-8')
#print(cvsfile[0])

from urllib.request import urlopen
from io import StringIO
import csv
url = urlopen('http://file.data.gov.tw/event/dataset.csv').read().decode('utf-8')
datafile = StringIO(url)
dicReader = csv.DictReader(datafile)
print(dicReader.fieldnames)
for row in dicReader:
    print(row)






#檔案型
'''
file = open("C:\Users\IMITA-PC-13\Desktop\dataset.csv")
reader = csv.reader(file)
data = list(reader)
print(data.decode('utf-8'))
'''


now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

print('資料抓取日期：' + now)

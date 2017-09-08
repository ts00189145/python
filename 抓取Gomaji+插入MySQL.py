'''
取得資料->解析->取代"與,->輸入資料庫（這邊有問題）*無法輸入
**20170907soup仍無法輸入資料庫要把之前的程式cp回來喔！
'''
#coding utf-8
#-*- coding: utf-8 -*-
import requests
import time
import pymysql
#使用requests套件、時間套件、Pymysql
from bs4 import BeautifulSoup
#使用BeauitfulSoup

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now


url = 'http://www.gomaji.com/index.php?city=Taiwan&category_id=264'


res = requests.get(url)
#從GoMaJi取回網頁程式碼



soup = BeautifulSoup(res.text,'lxml')

#print (soup)

soup1 = soup.prettify()#把soup變成string

'''可刪除
soup2 = soup1.replace('"',r'\"') #取代"為\"

soup3 = soup2.replace(",",r"\,") #取代,為\,
'''

db = pymysql.connect("localhost","testuser","test1234","testuser")
'''
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='testuser',
    passwd='test1234',
    db='testuser',
    charset='utf8'
)
'''
 # 使用cursor()方法获取操作游标 
cursor = db.cursor()



sql = "INSERT INTO test (url, website, code, time) VALUES ( '%s', '%s', '%s', '%s' )"
data = ( url, "http://www.gomaji.com", u'soup1 <a class="asd">ss</a>;中文 \r\n hhh', now)#20170908 1807發現soup不能輸入是中文的問題

try:
    cursor.execute(sql % data)
    # 執行sql語法
    db.commit()
    # 提交到資料庫執行
except:
    db.rollback()
    print ("MySQL DB Error")
    # 如果有錯誤則回滾
    db.close()
 # 關閉與資料庫的連接


print ('最新處理時間：'+ now)

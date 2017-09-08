'''
取得資料->解析名字價格網址->算出名字價格網址有多少個->帶入資料庫
**無法寫入資料庫
'''
#-*- coding: utf-8 -*-，
#coding = utf-8
import requests
import time
import pymysql.cursors
#使用requests套件、時間套件、Pymysql

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'http://www.gomaji.com/index.php?city=Taiwan&category_id=264'

res = requests.get(url0)
#從GoMaJi取回網頁程式碼

from bs4 import BeautifulSoup
#使用BeauitfulSoup

soup = BeautifulSoup(res.text,'html.parser')

#print (soup)

#以下是取出需要的資料------------------以下是第二階段
title = 'div.program h1'
#標題 *div.class名稱為program 裡面的h1
price = 'div.spe-pri h3'
#價格 *div.class名稱為spe-pri 裡面的h3
url1 = 'div.spe-pri a'
#超連結 *div.class名稱為spe-pri 裡面的a

title0 = soup.select(title)
price0 = soup.select(price)
url2 = soup.select(url1)
#帶入變數

title0len = len(title0)
price0len = len(price0)
url2len = len(url2)
#算出個別陣列有幾筆資料
'''
print("title0有:",len(title0),"個值") #了解這個陣列有多少值
print("price0:",len(price0),"個值") #了解這個陣列有多少值
print("url2:",len(url2),"個值") #了解這個陣列有多少值
'''
db = pymysql.connect("localhost","testuser","test1234","testuser")
#資料庫、使用者、密碼、資料庫

cursor = db.cursor()
#使用cursor()方法获取操作游标 

for i in range(0,len(title0),1):
    sql = 'INSERT INTO test1 (title, price, url, time) VALUES ( "%s", "%s", "%s", "%s" )'
    data = ( title0[i].text, price0[i].text, url2[i+2].get('href'), now)
    i = i + 1
    #上面url+2是因為前兩筆title是空的然後後面有
try:
    cursor.execute(sql % data)
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

print(sql)#語法是成功的但資料庫沒有資料輸入進去
print('資料抓取日期：' + now)

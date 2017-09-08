#20170907soup仍無法輸入資料庫要把之前的程式cp回來喔！
#這邊是要把網頁全部的程式碼insert進去資料庫
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

soup2 = soup1.replace('"',r'\"') #取代"為\"

soup3 = soup2.replace(",",r"\,") #取代,為\,


db = pymysql.connect("localhost","testuser","test1234","testuser")
 
 # 使用cursor()方法获取操作游标 
cursor = db.cursor()



sql = 'INSERT INTO test(url, website, code, time) \
        VALUES ( "%s", "%s", "%s", "%s" )' \
        % ( url, "http://www.gomaji.com", soup3, now)

try:
    cursor.execute(sql)
    # 執行sql語法
    db.commit()
    # 提交到資料庫執行
except:
    db.rollback()
    # 如果有錯誤則回滾
    db.close()
 # 關閉與資料庫的連接


print ('最新處理時間：'+ now)

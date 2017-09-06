#20170906soup仍無法輸入資料庫
import requests
import time
import pymysql

#使用requests套件、時間套件、Pymysql

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url = 'http://www.gomaji.com/index.php?city=Taiwan&category_id=264'

res = requests.get(url)
#從GoMaJi取回網頁程式碼

from bs4 import BeautifulSoup
#使用BeauitfulSoup

soup = BeautifulSoup(res.text,'html.parser')

#print (soup)

db = pymysql.connect("localhost","testuser","test1234","testuser" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

soup1 = soup.prettify()#把soup變成string

soup2 = soup1.replace('"',r'\"') #取代掉"

# SQL 插入语句(有問題無法用將變數插入SQL)*要取代soup裡面的"符號
sql = 'INSERT INTO test(url, website, code, time) \
      VALUES ( "%s", "%s", "%s", "%s" )' \
      % ( url, "http://www.gomaji.com", soup2, now)

try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()

# 关闭数据库连接
db.close()

print ('最新處理時間：'+ now)

#20170907soup仍無法輸入資料庫要把之前的程式cp回來喔！
import requests
import time
import pymysql.cursors
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

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='testuser',
                             password='test1234',
                             db='testuser',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `test` (`url`, `website` , `code` , `time`) VALUES (%s, %s,%s, %s)"
        cursor.execute(sql, (url, "http://www.gomaji.com", soup3, now))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
'''SELECT先不用看拉
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
'''
finally:
    connection.close()




print ('最新處理時間：'+ now)

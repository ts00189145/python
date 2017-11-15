# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup
import pymysql.cursors
#使用pymysql
import re
#使用正規
from selenium import webdriver

'''
db = pymysql.connect( #伺服器版本
    host='localhost',
    port=3306,
    user='coa',
    passwd='coa',
    db='web_crawler',
    charset='utf8'
)
'''
db = pymysql.connect( #本機測試版
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='open_data',
    charset='utf8'
)

cursor = db.cursor()

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y-%m-%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time


#所有網頁清單
urllist = ['http://www.hug.com.tw/hug/ProductList.aspx?MID=1',
           'http://www.hug.com.tw/hug/ProductList.aspx?MID=2',
           'http://www.hug.com.tw/hug/ProductList.aspx?MID=10']

#開啟瀏覽器
driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs for Windows
#driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe") #Windows
#driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')

#載入網址迴圈
urllen = len(urllist)
for link in range(urllen):
    print ('第',link,'個：', urllist[link])
    
    
    #將每一頁的筆數取回
    driver.get(urllist[link])  # 輸入網址，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
    
    allprod = []
    allurl = 'div.index_fo_name a'
    allurl0 = soup.select(allurl)
    urllen0 = len(allurl0)
    print('此頁面共' + str(urllen0) +'件商品')
    
    #印出頁面所有商品
    for urlnum in range(urllen0):
        #print('https://www.wonderfulfood.com.tw/Client/' + allurl0[urlnum].get('href'))
        allprod.append('https://www.wonderfulfood.com.tw/Client/' + allurl0[urlnum].get('href'))
        urlnum = urlnum +1
    print(allprod)
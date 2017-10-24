# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 11:07:41 2017

@author: IMITA-PC-13
"""

# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'http://www.tenha.com.tw/index.php?option=productm&lang=cht&task=pageinfo&id=1210&belongid=15&index=0'


from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
driver.get(url0)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
#print(pageSource)

soup = BeautifulSoup(pageSource,"lxml")
#將資料用lxml裝起來放置到soup

driver.quit()  # 關閉瀏覽器


#以下是取出需要的資料------------------以下是第二階段
images = 'div#imgView'
#介紹照片
title = 'div.productdetail h2'
#標題 *div.class名稱為product_introduction 裡面的h3
special_price = 'span.red16px2'
#特價


#資料轉換區
images0 = soup.select(images)
title0 = soup.select(title)
special_price0 = soup.select(special_price)


print('圖片：' , images0[0])#資料已經乾淨
print('標題：' , title0[0].text)#資料已經乾淨
print('特價：' , special_price0[0].text)#資料已經盡可能乾淨

print('資料抓取日期：' + now)
# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'http://www.gohappy.com.tw/shopping/Browse.do?op=vp&sid=12&cid=209655&pid=5613139'


from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
driver.get(url0)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
#print(pageSource)

soup = BeautifulSoup(pageSource,"lxml")
#將資料用lxml裝起來放置到soup

driver.quit()  # 關閉瀏覽器

#以下是取出需要的資料------------------以下是第二階段
images = 'img#bigimg'
#圖片
title = 'div.product_introduction h3'
#標題 *div.class名稱為product_introduction 裡面的h3
sintro = 'div.product_introduction dd'
#小介紹
original_price = 'dd.original_price '
#原價格
price = 'dd.list_price '
#價格
intro0 = 'div.descriptions '
#主介紹
specification = 'div.product_content'
#規格


#資料轉換區
images0 = soup.select(images)
title0 = soup.select(title)
sintro0 = soup.select(sintro)
original_price0 = soup.select(original_price)
price0 = soup.select(price)
intro1 = soup.select(intro0)
specification0 = soup.select(specification)

print('圖片：' , images0)#資料尚未乾淨
print('標題：' , title0[0].text)#資料已經乾淨
print('小介紹：' , sintro0[0].text)#資料已經盡可能乾淨
print('原價：' , original_price0[0].text)#資料已經盡可能乾淨
print('促銷價：' , price0[0].text)#資料已經盡可能乾淨
print('介紹區：' , intro1[0])#呈現原始碼
print('規格：' , specification0[0].text)#還蠻多空白的

print('資料抓取日期：' + now)
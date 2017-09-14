# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'https://www.myfone.com.tw/buy/index.php?action=product_detail&prod_no=P0000202302136'


from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
driver.get(url0)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
#print(pageSource)

soup = BeautifulSoup(pageSource,"lxml")
#將資料用lxml裝起來放置到soup

driver.quit()  # 關閉瀏覽器

#以下是取出需要的資料------------------以下是第二階段
title = 'div.itemRight h1'
#標題 *div.class名稱為product_introduction 裡面的h3
sintro = 'ul#W290_1 p'
#小介紹
price = 'div.red'#有點問題
#價格
intro0 = 'div.infoContent '
#主介紹

#資料轉換區
title0 = soup.select(title)
sintro0 = soup.select(sintro)
price0 = soup.select(price)
intro1 = soup.select(intro0)


print('標題：' , title0[0].text)#資料已經乾淨
print('小介紹：' , sintro0[0].text)#資料已經盡可能乾淨
print('價格：' , price0[0].text)#資料已經盡可能乾淨
print('介紹區：' , intro1[0])#資料已經盡可能乾淨

print('資料抓取日期：' + now)
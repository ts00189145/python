import requests
import time
#使用requests套件、時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup
now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
#取出今天日期、時間

today = time.strftime("%Y%m%d")
#取得今天的日期

url = 'http://24h.pchome.com.tw/onsale/v3/'+ today +'/'
#取得今天的網址

#print (url) 
#印出今天日期的URL


from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
driver.get(url)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
#print(pageSource)

soup = BeautifulSoup(pageSource,"lxml")
#將資料用lxml裝起來放置到soup
#print(soup)

driver.quit()  # 關閉瀏覽器





#以下是取出需要的資料------------------以下是第二階段
title = 'dl.onsale_box dd'
#標題

price = 'div.spe-pri h3'
#價格
url1 = 'div.spe-pri a'
#超連結（未完成）

articles0 = soup.select(title)
articles1 = soup.select(price)
articles2 = soup.select(url1)
#帶入變數

for art in articles0 + articles1 + articles2 :

   print(art)
   #print(art['href'],art.text)


print('資料抓取日期：' + now_data + ' ' + now_time)

import requests
import time
#使用requests套件、時間套件

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
#articles2 = soup.find_all(articles2['href'])
#帶入變數


for art in title0 + price0 + url2:
      print(art)
      print ('http://www.gomaji.com/' , art.get('href'))
      
print('資料抓取日期：' + now)

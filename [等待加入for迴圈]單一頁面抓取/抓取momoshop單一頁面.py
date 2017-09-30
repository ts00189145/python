# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=4999052&str_category_code=2001000056&mdiv=2001000056&Area=DgrpCategory'


from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
driver.get(url0)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
#print(pageSource)

soup = BeautifulSoup(pageSource,"lxml")
#將資料用lxml裝起來放置到soup

driver.quit()  # 關閉瀏覽器

#以下是取出需要的資料------------------以下是第二階段
images = 'img.jqzoom'
#介紹圖片
title = 'div.prdnoteArea h1'
#標題 *div.class名稱為product_introduction 裡面的h3
sintro = 'ul#categoryActivityInfo' 
#小介紹
original_price = 'ul.prdPrice del'
#原價
special_price = 'li.special'
#促銷價格
intro = 'iframe#ifrmGoods'
#主介紹
specification = 'div.attributesArea table'
#規格

#資料轉換區
images0 = soup.select(images)
title0 = soup.select(title)
sintro0 = soup.select(sintro)
original_price0 = soup.select(original_price)
special_price0 = soup.select(special_price)
intro0 = soup.select(intro)
specification0 = soup.select(specification)

print('標題：' , images0)#資料已經乾淨
print('標題：' , title0[0].text)#資料已經乾淨
print('小介紹：' , sintro0[0].text)#仍有問題
print('原價：' , original_price0[0].text)#資料已經乾淨
print('特價：' , special_price[0].text.rstrip().strip())#抓取到了
print('主介紹：' , intro0)#有點問題*******************
print('規格：' , specification0[0])#呈現原始碼

print('資料抓取日期：' + now)
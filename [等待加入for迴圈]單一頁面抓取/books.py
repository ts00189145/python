# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup
from urllib.request import urlopen

now_data = time.strftime("%Y-%m-%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'http://www.books.com.tw/web/sys_midm/food/1017?loc=P_002_1_003'

pageSource = urlopen(url0)

#from selenium import webdriver

#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
#driver.get(url0)  # 輸入網址，交給瀏覽器 
#pageSource = driver.page_source  # 取得網頁原始碼
#print(pageSource)

soup = BeautifulSoup(pageSource,"lxml")
#將資料用lxml裝起來放置到soup

#driver.quit()  # 關閉瀏覽器

#以下是取出需要的資料------------------以下是第二階段
main_images = 'div.cnt_mod002.cover_img img'#尚未完成
#圖片
main_name = 'div.mod.prd001  h1'
#標題 *div.class名稱為product_introduction 裡面的h3
original_price = 'ul.price li'
#原價
special_price = 'ul.price li'
#特價
file = 'div.sec_product01 '
#主介紹

#資料轉換區
main_images0 = soup.select(main_images)
main_name0 = soup.select(main_name)
original_price0 = soup.select(original_price)
special_price0 = soup.select(special_price)
file0 = soup.select(file)


try:
    main_images1 = main_images0[0]
except IndexError:
    main_images1 = 'Null'
    print(main_images1)
try:
    main_name1 = main_name0[0].text
except IndexError:
    main_name1 = 'Null'
    print(main_name1)
try:
    original_price1 = original_price0[0].text
except IndexError:
    original_price1 = 'Null'
    print(original_price1)
try:
    special_price1 =  special_price0[1].text
except IndexError:
    special_price1 = 'Null'
    print(special_price1)
try:
    file1 =  file0[0].text.strip('\n')
except IndexError:
    file1 = 'Null'
    print(file1)
    
#nowurl = allurl0[allprod].get('href')


print('圖片網址：',main_images1)#
print('標題：' , main_name1)#資料已經乾淨
print('原價：' , original_price1)#資料已經盡可能乾淨
print('特價：' , special_price1)#資料已經盡可能乾淨
print('介紹區：' , file1)#資料已經盡可能乾淨
print('現在網址：' , url0 )

print('資料抓取日期：' + now)
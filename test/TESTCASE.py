# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup
from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

now_data = time.strftime("%Y-%m-%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now



url = 'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=74'

#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe") #Windows
driver.get(url)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource,"lxml")
driver.quit()  # 關閉瀏覽器

#以下是取出需要的資料------------------以下是第二階段
allurl = 'h5.nick a'
allurl0 = soup.select(allurl)
print(allurl0[0].get('href'))
#網址-------------------------------------

main_images = 'div.gallery img'
main_images0 = soup.select(main_images)
imgnum= 0
main_images1 = []
imglen = len(main_images0)
for imgnum in range(imglen):
    #main_images1 = main_images0[imgnum]['src']
    main_images1.append(main_images0[imgnum]['src'])
    #print(main_images1)
    print('圖片網址：',main_images0[imgnum]['src'])
print('圖片網址：',main_images0[0]['src'])
#圖片-------------------------------------

main_name = 'li.menu_cy'
main_name0 = soup.select(main_name)
print('標題：' , main_name0[0].text)
#標題-----------------------------------

original_price = 'span.price_web strong span'
original_price0 = soup.select(original_price)
print('原價：' , original_price0[0].text)
#原價-----------------------------------

special_price = ''
special_price0 = soup.select(special_price)
print('特價：' , special_price0[0].text)
#特價---------------------------------

file = 'div.txt_cy'
file0 = soup.select(file)
print('介紹區：' , file0[0].text)
#主介紹------------------------------------

specification = 'dd.content-blk'
specification0 = soup.select(specification)
print('規格：' ,specification0[0].text)
#規格

'''
num = "$1,190元起"
import re
num1 = num.replace(',','')
result = re.findall(r'[-+]?\d*\,\.\d+|\d+', num1)[0]
'''

nexpag = driver.find_element_by_partial_link_text('下一頁')
try:
    #找到要做的事情
    print('有下一頁')
    nexpag.click()
except NoSuchElementException:
    #找不到异常处理
    print ("no next page")


#-----------以下暫時用不到------------------------------------------
#資料轉換區
allurl0 = soup.select(allurl)
main_images0 = soup.select(main_images)
main_name0 = soup.select(main_name)
original_price0 = soup.select(original_price)
special_price0 = soup.select(special_price)
file0 = soup.select(file)
specification0 = soup.select(specification)


print(allurl0[0].get('href'))
print('圖片網址：',main_images0)#
print('標題：' , main_name0)#資料已經乾淨
print('原價：' , original_price0)#資料已經盡可能乾淨
print('特價：' , special_price0)#資料已經盡可能乾淨
print('介紹區：' , file0)#資料已經盡可能乾淨
print('規格：' ,specification0 )
print('現在網址：' , url )


#----------------------------------------------------------------------

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
    original_price2 = re.findall('[0-9]+',original_price1)
except IndexError:
    original_price1 = 'Null'
    print(original_price1)
try:
    special_price1 =  special_price0[1].text
    special_price2 = re.findall('[0-9]+',special_price1)
except IndexError:
    special_price1 = 'Null'
    print(special_price1)
try:
    file1 =  file0[0].text.strip('\n')
except IndexError:
    file1 = 'Null'
    print(file1)
try:
    specification1 =  specification0[0]
except IndexError:
    specification1 = ''
    #print(specification1)
    

print('圖片網址：',main_images1)#
print('標題：' , main_name1)#資料已經乾淨
print('原價：' , original_price1)#資料已經盡可能乾淨
print('特價：' , special_price1)#資料已經盡可能乾淨
print('介紹區：' , file1)#資料已經盡可能乾淨
print('現在網址：' , url )

print('資料抓取日期：' + now)
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

from selenium.common.exceptions import NoSuchElementException
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
urllist = ['https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=74',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=68',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=94',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=91',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=89',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=63',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=80',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=121',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=95',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=118',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=104',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=102',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=45',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=79',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=125',
'https://www.wonderfulfood.com.tw/Client/list_fo.aspx?class=134']

#開啟瀏覽器
#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs for Windows
driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe") #Windows
#driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')

allprod = []


#載入類別網址
urllen = len(urllist)
for link in range(urllen):
    print ('第',link,'個：', urllist[link])
    
    
    #將每一頁的筆數取回
    driver.get(urllist[link])  # 輸入網址，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
    
    next_page = ''
    main_name = 'li.menu_cy'
    main_name0 = soup.select(main_name)
    print('標題：' , main_name0[0].text)
    
    nexpag = driver.find_element_by_partial_link_text('下一頁')
    
    while nexpag is True:
        #取得商品URL
        allurl = 'div.index_fo_name a'
        allurl0 = soup.select(allurl)
        urllen0 = len(allurl0)
        print('此頁面共' + str(urllen0) +'件商品')
        #印出頁面所有商品
        for urlnum in range(urllen0):
            print('https://www.wonderfulfood.com.tw/Client/' + allurl0[urlnum].get('href'))
            allprod.append('https://www.wonderfulfood.com.tw/Client/' + allurl0[urlnum].get('href'))
            urlnum = urlnum +1
            
         #點擊下一頁
         nexpag.click()
            nexpag = driver.find_element_by_partial_link_text('下一頁')#-----------------------------------可以點擊但是不知道怎麼讓它重複
        #重新取得一次頁面所有商品
        #再點擊下一頁
        #如果沒有下一頁就跳出
            print(allprod)#已取得所有頁數商品
        
    
    
    
    
    
    #取得總頁數---------------------------這邊不知道怎麼辦
    page = 'div.pager'
    page0 = soup.select(page)
    strpage = int(page0[0].text) #取得總頁數
    
    
    
    
    
    for pagenum in range(1,strpage+1):
        url1 = 'http://www.books.com.tw/web/sys_midm/food/1017?o=5&page=' + str(pagenum)
        print('第'+ str(pagenum) +'頁')
        #print(url1)
        pagenum = pagenum + 1
        
        #送出頁數
        driver.get(url1)
        pageSource = driver.page_source  # 取得網頁原始碼
        soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
        #time.sleep(1)
        
        #取得頁面所有的超連結-----------------------這邊不知道為什麼一直都是100而且都是重複的
        allurl = 'div.index_fo_name a'
        allurl0 = soup.select(allurl)
        urllen0 = len(allurl0)
        print('此頁面共' + str(urllen0) +'件商品')
    
        
        
        #將所有取得的超連結做for迴圈將資料寫入資料庫
        for allprod in range(0,urllen0):
            #print (allurl0[allprod].get('href'))
            print('第',allprod,'樣商品，共計',urllen0,'樣')
            
            driver.get(allurl0[allprod].get('href'))  # 輸入超連結，交給瀏覽器 
            pageSource = driver.page_source  # 取得網頁原始碼
            soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
            
            
           #以下是取出需要的資料------------------以下是第二階段
            main_images = 'div.inside_product_detail_img img'
            #主要圖片
            main_name = 'div.inside_product_detail_name '
            #主標題
            original_price = 'div.inside_product_detail_price_fixed span'
            #原價
            special_price = 'div.inside_product_detail_price_sp span'
            #特價
            file = 'div.title_side_product_detail_about_box'
            #文案文字
            specification = 'table.product_detail_weight'
            #規格
            
            #資料轉換區
            main_images0 = soup.select(main_images)
            main_name0 = soup.select(main_name)
            original_price0 = soup.select(original_price)
            special_price0 = soup.select(special_price)
            file0 = soup.select(file)
            specification0 = soup.select(specification)
            
            #資料取出及測試區，如果沒有資料則輸入空白
            try:
                #main_images1 = main_images0[0]
                imgnum= 0
                main_images1 = []
                imglen = len(main_images0)
                for imgnum in range(imglen):
                    main_images1.append(main_images0[imgnum]['src'])
            except IndexError:
                main_images1 = ''
                #print(main_images1)
                
            try:
                main_name1 = main_name0[0].text
            except IndexError:
                main_name1 = ''
                #print(main_name1)
                
            try:
                original_price1 = original_price0[0].text.replace(',','')
                original_price2 = re.findall(r'[-+]?\d*\.\d+|\d+', original_price1)[0]
            except IndexError:
                original_price2 = ''
                #print(original_price1)
                
            try:
                special_price1 = special_price0[1].text.replace(',','')
                special_price2 = re.findall(r'[-+]?\d*\.\d+|\d+', special_price1)[0]
            except IndexError:
                special_price2 = ''
                #print(special_price1)
                
            try:
                file1 =  file0[0].text.strip('\n')
            except IndexError:
                file1 = ''
                #print(file1)
            
            try:
                specification1 =  specification0[0].text.strip('\n')
            except IndexError:
                specification1 = ''
                #print(specification1)
            
            nowurl = allurl0[allprod].get('href')
            
            
            '''
            try:
                print('圖片網址：',main_images1)#
                print('標題：' , main_name1)#資料已經乾淨
                print('原價：' , original_price2)#資料已經盡可能乾淨
                print('特價：' , special_price2)#資料已經盡可能乾淨
                print('介紹區：' , file1)#資料已經盡可能乾淨
                print('資料抓取日期：' + now)
            except:
                print(allurl0[allprod].get('href')+"  *******有問題*******  ")
            
            '''
            try:
                # success
                cursor.execute('INSERT INTO ' + ' books (main_images, main_name, original_price, special_price, file, url, time) ' + ' VALUES (%s,%s,%s,%s,%s,%s,NOW()) ' ,
                               ( str(main_images1), str(main_name1), str(original_price2),str(special_price2), str(file1), str(nowurl) ) ) 
                # success
                # 執行sql語法
                db.commit()
                # 提交到資料庫執行
            except:
                db.rollback()
                print ("MySQL DB Error")
                # 如果有錯誤則回滾
                db.close()
                # 關閉與資料庫的連接
            #time.sleep(1) #休息兩秒
    
driver.quit()  # 關閉瀏覽器
print('資料抓取日期：' + now)

#這是有出現總頁數且容易取得的爬蟲

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
    db='web_crawler',
    charset='utf8'
)
'''
cursor = db.cursor()

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y-%m-%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

#起始頁
urllist = ['http://www.ttmall.com.tw/Product/366/%E6%9C%89%E6%A9%9F%E7%B1%B3',
           'http://www.ttmall.com.tw/Product/367/%E6%9C%89%E6%A9%9F%E8%94%AC%E8%8F%9C',
           'http://www.ttmall.com.tw/Product/131/%E7%B1%B3%E9%A3%9F%E9%BA%B5%E9%A1%9E',
           'http://www.ttmall.com.tw/Product/138/%E6%99%82%E4%BB%A4%E8%94%AC%E6%9E%9C']




#啟動瀏覽器將網頁資料取回
#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs for Windows
#driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe") #Windows
driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')


urllen = len(urllist)
for link in range(urllen):#取出第link個連結
    print ('第',link,'個：', urllist[link])
    driver.get(urllist[link])  # 輸入網址，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
    
    page = 'li.display strong'
    page0 = soup.select(page)
    strpage = int(page0[1].text) #取得總頁數
    print('共計'+ str(strpage) +'頁')
    #link = link + 1
    
    for pagenum in range(strpage):#跑頁數
        url1 = urllist[link] +'?page='+ str(pagenum+1)
        print('第'+ str(pagenum) +'頁')
        print(url1)
        pagenum = pagenum + 1
        
        #送出頁數
        driver.get(url1)
        pageSource = driver.page_source  # 取得網頁原始碼
        soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
        #time.sleep(1)
        
        #取得頁面所有的超連結
        allurl = 'ul.commodity.cy_list li a'
        allurl0 = soup.select(allurl)
        urllen0 = len(allurl0)
        print('此頁面共' + str(urllen0) +'件商品')
    
        
        
        #將所有取得的超連結做for迴圈將資料寫入資料庫
        for allprod in range(0,urllen0):
            #print (allurl0[allprod].get('href'))
            print('第',allprod+1,'樣商品，共計',urllen0,'樣')
            
            driver.get(allurl0[allprod].get('href'))  # 輸入超連結，交給瀏覽器 
            pageSource = driver.page_source  # 取得網頁原始碼
            soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup

            #資料取出及測試區，如果沒有資料則輸出空白
            try:#主要商品圖
                main_images = 'a#product-img-lightbox img'
                main_images0 = soup.select(main_images)
                #main_images1 = main_images0[0]
                imgnum= 0
                main_images1 = []
                imglen = len(main_images0)
                for imgnum in range(imglen):
                    main_images1.append('http://cbfa.ttmall.com.tw/'+main_images0[imgnum]['src'])
            except IndexError:
                main_images1 = ''
                #print(main_images1)
                
            try:#主要商品名稱
                main_name = 'li.menu_cy'
                main_name0 = soup.select(main_name)
                main_name1 = main_name0[0].text
            except IndexError:
                main_name1 = ''
                #print(main_name1)
                
            try:#原價
                original_price = 'span.price_web strong span'
                original_price0 = soup.select(original_price)
                original_price1 = original_price0[0].text.replace(',','')
                original_price2 = re.findall(r'[-+]?\d*\.\d+|\d+', original_price1)[0]
            except IndexError:
                original_price2 = ''
                #print(original_price1)
                
            try:#特價
                special_price = 'strong.price01'
                special_price0 = soup.select(special_price)
                special_price1 = special_price0[0].text.replace(',','')
                special_price2 = re.findall(r'[-+]?\d*\.\d+|\d+', special_price1)[0]
            except IndexError:
                special_price2 = ''
                #print(special_price1)
                
            try:#文案
                file = 'div.txt_cy'
                file0 = soup.select(file)
                file1 =  file0[0].text.strip('\n')
            except IndexError:
                file1 = ''
                #print(file1)
                
            try:
                specification = 'dd.content-blk'
                specification0 = soup.select(specification)
                specification1 =  specification0[0].text.strip('\n')
            except IndexError:
                specification1 = ''
                #print(specification1)
            
            nowurl = allurl0[allprod].get('href')
            

            try:
                # success
                cursor.execute('INSERT INTO ' + ' ttmall (main_images, main_name, original_price, special_price, file, url ,specification, time) ' + ' VALUES (%s,%s,%s,%s,%s,%s,%s,NOW()) ' ,
                               ( str(main_images1), str(main_name1), str(original_price2),str(special_price2), str(file1), str(nowurl) ,str(specification1) ) ) 
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

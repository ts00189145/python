# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:31:59 2017

@author: IMITA-PC-13
"""

# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup
import pymysql.cursors

db = pymysql.connect(
    host='192.168.1.74',
    port=3306,
    user='root',
    passwd='official',
    db='web_crawler',
    charset='utf8'
)
'''
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='open_data',
    charset='utf8'
)
'''
cursor = db.cursor()

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

starturl = 'http://www.gomaji.com/index.php?city=Taiwan&category_id=31'
#起始頁

#將網頁資料取回
from selenium import webdriver
#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
#driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe")
driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
#webdriver.PhantomJS(service_log_path=path)

driver.get(starturl)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup


    
#取得頁面所有的超連結
allurl = 'div.spe-pri a'
allurl0 = soup.select(allurl)
urllen0 = len(allurl0)
print('共' + str(urllen0) +'件')
    
    #將所有取得的超連結做for迴圈將資料寫入資料庫
for allprod in range(0,urllen0):
    #print (allurl0[allprod].get('href'))
        
    driver.get('http://www.gomaji.com/'+allurl0[allprod].get('href'))  # 輸入超連結，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
    
    
    #以下是取出需要的資料------------------以下是第二階段
    main_images = 'div.gallery'
    #圖片
    main_name = 'div.today-new-block h1'
    #標題 *div.class名稱為product_introduction 裡面的h3
    special_price = 'div.product-status  p'
    #價格
    file = 'div.intro-wrap p'
    #主介紹
    
    #資料轉換區
    main_images0 = soup.select(main_images)
    main_name0 = soup.select(main_name)
    special_price0 = soup.select(special_price)
    file0 = soup.select(file)
    
    '''
    try:
        #print('圖片網址：',main_images0[0])#
        print('標題：' , main_name0[0].text.strip('\n'))#資料已經乾淨
        print('第' + str(allprod) + '個')
        #print('價格：' , special_price0[1].text)#資料已經盡可能乾淨
        #print('介紹區：' , file0)#資料已經盡可能乾淨
    except:
        print(allurl0[allprod].get('href')+"  *****有問題*******")
    '''
    try:
        main_images1 = main_images0[0]
    except IndexError:
        main_images1 = ''
        #print(main_images1)
            
    try:
        main_name1 = main_name0[0].text.strip('\n')
    except IndexError:
        main_name1 = ''
        #print(main_name1)
    
    try:
        special_price1 =  special_price0[1].text
    except IndexError:
        special_price1 = ''
        #print(special_price1)
            
    try:
        file1 =  file0[0].text.strip('\n')
    except IndexError:
        file1 = ''
        #print(file1)
    nowurl = 'http://www.gomaji.com/'+allurl0[allprod].get('href')

    try:
        # success
        cursor.execute('INSERT INTO '+ ' gomaji (main_images, main_name, special_price, file, time, url)' +' VALUES(%s,%s,%s,%s,NOW(),%s)', ( str(main_images1), str(main_name1), str(special_price1), str(file1), str(nowurl) ) ) 
        #print('INSERT INTO '+ ' gomaji (main_images, main_name, special_price, file, time, url)' +' VALUES(%s,%s,%s,%s,NOW(),%s)', ( str(main_images1), str(main_name1), str(special_price1), str(file1), str(nowurl) ) ) 
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
        
#db.close()
driver.quit()  # 關閉瀏覽器
print('資料抓取日期：' + now)
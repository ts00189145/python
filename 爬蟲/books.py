# -*- coding: utf-8 -*-
import time
#使用時間套件
from bs4 import BeautifulSoup
#使用BeauitfulSoup
import pymysql.cursors
#使用pymysql


#真正伺服器IP
db = pymysql.connect(
    host='192.168.1.74',
    port=3306,
    user='root',
    passwd='official',
    db='web_crawler',
    charset='utf8'
)
'''
#測試伺服器IP
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
now_data = time.strftime("%Y-%m-%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

starturl = 'http://www.books.com.tw/web/sys_midm/food/1017?loc=P_002_1_003'
#起始頁

#將網頁資料取回
from selenium import webdriver
#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs for Windows
#driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe") #Windows
driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
#webdriver.PhantomJS(service_log_path=path)



driver.get(starturl)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup

page = 'div.page span'
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
    time.sleep(2)
    
    #取得頁面所有的超連結-----------------------這邊不知道為什麼一直都是100而且都是重複的
    allurl = 'a.cover.cov_a'
    allurl0 = soup.select(allurl)
    urllen0 = len(allurl0)
    print('此頁面共' + str(urllen0) +'件商品')

    
    
    #將所有取得的超連結做for迴圈將資料寫入資料庫
    for allprod in range(0,urllen0):
        #print (allurl0[allprod].get('href'))
        
        driver.get(allurl0[allprod].get('href'))  # 輸入超連結，交給瀏覽器 
        pageSource = driver.page_source  # 取得網頁原始碼
        soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
        
        
       #以下是取出需要的資料------------------以下是第二階段
        main_images = 'div.cnt_mod002.cover_img img'#尚未完成
        #主要圖片
        main_name = 'div.mod.prd001 h1'
        #主標題
        original_price = 'ul.price li'
        #原價
        special_price = 'ul.price li'
        #特價
        file = 'div.sec_product01 '
        #文案文字
        
        #資料轉換區
        main_images0 = soup.select(main_images)
        main_name0 = soup.select(main_name)
        original_price0 = soup.select(original_price)
        special_price0 = soup.select(special_price)
        file0 = soup.select(file)
        
        #資料取出及測試區，如果沒有資料則輸入空白
        try:
            main_images1 = main_images0[0]
        except IndexError:
            main_images1 = ''
            #print(main_images1)
            
        try:
            main_name1 = main_name0[0].text
        except IndexError:
            main_name1 = ''
            #print(main_name1)
            
        try:
            original_price1 = original_price0[0].text
        except IndexError:
            original_price1 = ''
            #print(original_price1)
            
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
        
        nowurl = allurl0[allprod].get('href')
        
        
        '''
        try:
            print('圖片網址：',main_images1)#
            print('標題：' , main_name1)#資料已經乾淨
            print('原價：' , original_price1)#資料已經盡可能乾淨
            print('特價：' , special_price1)#資料已經盡可能乾淨
            print('介紹區：' , file1)#資料已經盡可能乾淨
            print('資料抓取日期：' + now)
        except:
            print(allurl0[allprod].get('href')+"  *******有問題*******  ")
        
        '''
        try:
            # success
            cursor.execute('INSERT INTO ' + ' books (main_images, main_name, original_price, special_price, file, url, time) ' + ' VALUES (%s,%s,%s,%s,%s,%s,NOW()) ' , 
                           ( str(main_images1), str(main_name1), str(original_price1),str(special_price1), str(file1), str(nowurl) ) ) 
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
        time.sleep(2) #休息兩秒
    
driver.quit()  # 關閉瀏覽器
print('資料抓取日期：' + now)

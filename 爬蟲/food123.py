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

now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time
#取出今天日期、時間，並整成變數now

url0 = 'https://www.food123.com.tw/site/category/502/%E5%84%AA%E8%B3%AA%E9%AE%AE%E8%94%AC%E6%9E%9C'
#起始頁

#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
#driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe")
driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')


driver.get(url0)  # 輸入網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
#print(pageSource)


#取得所有的超連結
allurl = 'a.item-wrap.border-grey.bg-white'
allurl0 = soup.select(allurl)
urllen0 = len(allurl0)
print('此頁面共' + str(urllen0) +'件商品')


for allprod in range(0,urllen0):
    print('第',allprod,'樣商品，共計',urllen0,'樣')
    driver.get('https://www.food123.com.tw'+allurl0[allprod].get('href'))  # 輸入超連結，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pageSource,"lxml") #將資料用lxml裝起來放置到soup
    #time.sleep(2)
    
    #以下是取出需要的資料------------------以下是第二階段
    main_images = 'img.item-img'
    #介紹照片
    main_name = 'h1.title'
    #標題 *div.class名稱為product_introduction 裡面的h3
    original_price = 'div.flex.text-center del'
    #原價
    special_price = 'span.site-color.big-price'
    #特價
    file = 'article.detail-intro.markdown-body.editormd-html-preview'
    #主介紹
    specification = 'article.detail-info.markdown-body.editormd-html-preview'
    #規格
    
    #資料轉換區
    main_images0 = soup.select(main_images)
    main_name0 = soup.select(main_name)
    original_price0 = soup.select(original_price)
    special_price0 = soup.select(special_price)
    file0 = soup.select(file)
    specification0 = soup.select(specification)
    
    
    #資料測試區
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
        main_name1 = main_name0[0].text.strip('\n')
    except IndexError:
        main_name1 = ''
        #print(main_name1)
    try:
        original_price1 = original_price0[0].text.replace(',','')
        original_price2 = re.findall(r'[-+]?\d*\.\d+|\d+', original_price1)[0]
    except IndexError:
        original_price1 = ''
        #print(original_price1)
            
    try:
        special_price1 = special_price0[0].text.replace(',','')
        special_price2 = re.findall(r'[-+]?\d*\.\d+|\d+', special_price1)[0]
    except IndexError:
        special_price1 = ''
        #print(special_price1)
            
    try:
        file1 =  file0[0].text.strip('\n')
    except IndexError:
        file1 = ''
        #print(file1)
    
    try:
        specification1 =  specification0[0].text
    except IndexError:
        specification1 = ''
        #print(specification1)
    nowurl = 'https://www.food123.com.tw'+allurl0[allprod].get('href')
    
    '''
    try:
        #print('圖片：' , main_images1) #資料已經乾淨
        print('標題：' , main_name1) #資料已經乾淨
        #print('原價：' , original_price2) #資料已經盡可能乾淨
        #print('特價：' , special_price2)#資料已經盡可能乾淨
        #print('介紹區：' , file1) #資料已經盡可能乾淨
        #print('規格：' , specification1)
        print('網址為：','https://www.food123.com.tw'+allurl0[a].get('href'))
    except:
        print('有點問題')
    '''
    try:
        cursor.execute('INSERT INTO '+ ' food123 (main_images ,main_name , original_price ,special_price ,file ,specification ,url ,time )' +' VALUES (%s,%s,%s,%s,%s,%s,%s,NOW()) ' ,
                       (str(main_images1), str(main_name1), str(original_price2), str(special_price2), str(file1), str(specification1), str(nowurl) ) )
        # 執行sql語法
        db.commit()
        # 提交到資料庫執行
    except:
        db.rollback()
        print ("MySQL DB Error")
        # 如果有錯誤則回滾
        db.close()
        #關閉與資料庫的連接
    

driver.quit()  # 關閉瀏覽器
print('資料抓取日期：' + now)

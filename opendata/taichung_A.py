# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 14:02:21 2017

@author: IMITA-PC-13
"""

import time
from selenium.webdriver.support.ui import Select
import pandas as pd
import pymysql.cursors


'''
#真正伺服器IP
db = pymysql.connect(
    host='192.168.1.74',
    port=3306,
    user='root',
    passwd='official',
    db='open_data',
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

cursor = db.cursor()

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y-%m-%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

starturl = 'http://mkis.taichung.gov.tw/PIS/query.jsp'
#起始頁
year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d")

#將網頁資料取回
from selenium import webdriver
#driver = webdriver.PhantomJS(executable_path=r'C:\Users\IMITA-PC-13\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs for Windows
driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe") #Windows
#driver = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
#webdriver.PhantomJS(service_log_path=path)

driver.get(starturl)  # 輸入網址，交給瀏覽器 


#主要欄位與次要欄位
tbXP = driver.find_element_by_id('tbXP').click()

tbYD = driver.find_element_by_id('tbYD').click()

#日期選擇區
sltA1_1 = Select(driver.find_element_by_name('y1'))
sltA1_1.select_by_visible_text("2017")

sltA1_2 = Select(driver.find_element_by_name('m1'))
sltA1_2.select_by_visible_text("1")

sltA1_3 = Select(driver.find_element_by_name('d1'))
sltA1_3.select_by_visible_text("2")

sltA2_1 = Select(driver.find_element_by_name('y2'))
sltA2_1.select_by_visible_text("2017")

sltA2_2 = Select(driver.find_element_by_name('m2'))
sltA2_2.select_by_visible_text("1")

sltA2_3 = Select(driver.find_element_by_name('d2'))
sltA2_3.select_by_visible_text("2")

#市場條件與產品條件（全選）
MI00ID = driver.find_element_by_id('MI00ID').click()

PI00ID = driver.find_element_by_id('PI00ID').click()

#製表
driver.find_element_by_id('DIV_4').click()


driver.switch_to_window(driver.window_handles[1])
time.sleep(60)
#print(driver.page_source)
data = pd.read_html(driver.page_source)

tableName = "taichung_A" #資料表名稱

#建立資料表(先檢查是否已存在)
cursor.execute('SELECT COUNT(*) AS num FROM `information_schema`.`TABLES` WHERE TABLE_NAME="'+tableName+'" AND TABLE_SCHEMA="open_data"')
if cursor.fetchone()[0] == 0:
    createSQL = 'CREATE TABLE IF NOT EXISTS `open_data`.`'+tableName+'` ('+(','.join('`'+data.columns+'` VARCHAR(200)'))+') ENGINE=MYISAM CHARSET=utf8;'
    cursor.execute( createSQL )
else:
    print('資料表"open_data.'+tableName+'"已存在，不用新建')
        
#匯入SQL語法的前半部，這部份大家都一樣
SQL_head = 'insert into '+'`'+tableName+'` ( ' + (','.join('`'+data.columns+'`')) + ' )'\
            +' values('+(' %s,'*len(data.columns))[0:-1] +' )'
#print( 'SQL_head:'+SQL_head+'\n' )


#把所有要執行的SQL語法都放進SQLs裡面
SQLs = list()
SQL_values = list()
for sn in data.index:
    tmp = list()
    for col in data.columns:
        tmp.append( str( data[col][sn] ) )
    SQL_values.append(tuple(tmp))


#所有SQL語法執行一遍
sn = 1
retry = 0 #SQL執行失敗重試次數
retryError = 0 #SQL執行失敗重試後還是失敗次數
totalRow = len(data.index)
for SQL_value in SQL_values:
    try:
        cursor.execute( SQL_head, SQL_value )
    except:
        time.sleep(1)
        retry += 1
        try:
            cursor.execute( SQL_head, SQL_value )
        except:
            retryError += 1
            print(SQL_value)
    if sn%100 == 1:
        print('進度：'+str(sn)+'/'+str(totalRow))
    sn += 1

print('結束，重試'+str(retry)+'次，失敗'+str(retryError)+'次')
#關閉資料庫連結
db.close()

#driver.quit()  # 關閉瀏覽器
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:34:05 2017

@author: IMITA-PC-13
"""
#帶入套件
import pymysql.cursors
import pandas as pd
import time

#抓回資料
data = pd.read_json('http://edbkcg.kcg.gov.tw/prices/PricesToJson.php')

#取出今天日期、時間，並整成變數now
now_data = time.strftime("%Y/%m/%d")
now_time = time.strftime("%H:%M:%S")
now = now_data + ' ' + now_time

#去抓特定欄位
up_price = data.T.loc['上價']
down_price = data.T.loc['下價']
center_price = data.T.loc['中價']
transaction_date = data.T.loc['交易日期']
amount = data.T.loc['交易量']
crop_code = data.T.loc['作物代號']
crop_name = data.T.loc['作物名稱']
market_code = data.T.loc['市場代號']
market_name = data.T.loc['市場名稱']
average_price = data.T.loc['平均價']

#連線DB
db = pymysql.connect(
        host='localhost',
        port=3306,
        user='testuser',
        passwd='test1234',
        db='testuser',
        charset='utf8'
    )

cursor = db.cursor()

for i in range(len(data)):
    #print(i)
    #input_to_db(organ,dataname,browse,download,score,i)
    cursor.execute('insert into ' + ' data02 (up_price, down_price, center_price, transaction_date, amount, crop_code,crop_name,market_code,market_name,average_price,now )' + 
                   ' values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                   (str( up_price.iloc[i] ) ,
                    float ( down_price.iloc[i] ),
                    str( center_price.iloc[i]),
                    str( transaction_date.iloc[i]) ,
                    str( amount.iloc[i]) ,
                    str( crop_code.iloc[i] ) ,
                    str( crop_name.iloc[i] ),
                    str( market_code.iloc[i]),
                    str( market_name.iloc[i]) ,
                    str( average_price.iloc[i]) ,                     
                    str( now ) ) )

try:
    # 執行sql語法
    db.commit()
    # 提交到資料庫執行
    print("成功插入")
    db.close()
except:
    db.rollback()
    print ("MySQL DB Error")
    # 如果有錯誤則回滾
    db.close()
    # 關閉與資料庫的連接

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:39:16 2017

@author: IMITA-PC-13
"""

import requests
import xml.etree.cElementTree as ET

url = "https://data.fda.gov.tw/cacheData/35_1.xml"
reqs = requests.get(url)
tree = ET.ElementTree(reqs.text)
root = tree.getroot()
root0 = ET.fromstring(root)

#可以印出資料了----------------只能取出單一資料還不能全部取出
for row in root0.iter('rows'):
    for col in row:
        print(col.tag)#資料欄位
        print(col.text + col)#資料內容


#還沒有做完


   
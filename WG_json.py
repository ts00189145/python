# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:21:17 2017

@author: IMITA-PC-13
"""
#帶入套件
import pymysql.cursors
import pandas as pd
import json
import codecs

def lstrip_bom(str_, bom="BOM_UTF8"):
    if str_.startswith(bom):
        return str_[len(bom):]
    else:
        return str_

#jj = json.loads(lstrip_bom(open('WG.json').read()))
#print(jj)

#jj=json.loads( codecs.open('WG.json', 'r', 'utf-8-sig') )
#print(jj)

with open('WG.json','r') as jOpen:
	jData = jOpen.read()
	jj=json.loads(jData.decode('utf-8-sig'))	
	print(jj)


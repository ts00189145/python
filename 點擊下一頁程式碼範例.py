# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:00:57 2017

@author: IMITA-PC-13
"""

from selenium import webdriver
driver = webdriver.Chrome(r"C:\selenium_driver_chrome\chromedriver.exe")
driver.get('http://www.books.com.tw/web/sys_midm/food/1017?loc=P_002_1_003')
'''
try:
    elem =driver.find_element_by_class_name('nxt')
    print('find',elem.tag_name)
except:
    print('not find')
'''
elem =driver.find_element_by_class_name('nxt')
elem.click()

driver.quit()  # 關閉瀏覽器
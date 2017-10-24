# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
#使用BeauitfulSoup
from urllib.request import urlopen
import os

url0 = 'http://www.books.com.tw/products/N010808045?loc=P_004_003'

pageSource = urlopen(url0)

soup = BeautifulSoup(pageSource,"lxml")

main_images = 'div.cnt_mod002.cover_img img'#尚未完成

main_images0 = soup.select(main_images)

images = main_images0[0].get('src')







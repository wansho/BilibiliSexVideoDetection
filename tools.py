# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:05:58 2018

@author: wansho
"""

from bs4 import BeautifulSoup
import re

'''
用beautifulsoap 修补一下html,xml
'''
def fix_html(source):
    # 修补html
    soup = BeautifulSoup(source)
    fixed_source = soup.prettify()
    
    return fixed_source

'''
按行读取文本内容，并返回list
'''
def load_readlines(path):
    fr = open(path, 'r', encoding = 'utf-8')
    danmu_list = fr.readlines()
    fr.close()
    return danmu_list

'''
加载xml文件
'''
def load_xml(path):
    fr = open(path, 'r', encoding = 'utf-8')
    source = fr.read()
    fr.close()
    return source

'''
将弹幕list按行写入TXT文件
'''
def write_danmu(path,danmu_list):
    fw = open(path, 'w', encoding = 'utf-8')
    for danmu in danmu_list:
        fw.write(danmu + '\n')
    fw.flush()
    fw.close()

'''
解析xml文件获取弹幕列表
'''
def parse_xml(source):
    
    soup = BeautifulSoup(source)
    # 获取包含 class 为 c ，存在id属性的 div  很重要
    danmus = soup.find_all('d',  p = re.compile('.*'))
    
    # print(len(danmus))
    
    danmu_list = []
    
    for danmu in danmus:
        content = danmu.get_text().strip()
        danmu_list.append(content)
        
    return danmu_list    
  
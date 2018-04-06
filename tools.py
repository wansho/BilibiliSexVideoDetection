# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:05:58 2018

1、对xml文件进行解析

@author: wansho
"""

from bs4 import BeautifulSoup
import re
import os

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
将弹幕列表写入TXT文件
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
    

'''
将xml文件中的弹幕提取到 parsed_danmu 文件夹下 的TXT文件中

config 表示是对sex 文件进行处理还是notsex文件进行处理
'''
def parse_danmu(config): 
    abs_path = os.path.abspath('.')
    xml_dir = abs_path + '\\xml\\' + config
    write_dir = abs_path + '\\train\\' + config
    
    files = os.listdir(xml_dir)
    for file in files:
        path = xml_dir + '\\' + file
        source = load_xml(path)
        
        fixed_source = fix_html(source)
        
        danmu_list = parse_xml(fixed_source)
        
        write_path = write_dir + '\\train_' + file
        write_danmu(write_path,danmu_list)
    
     
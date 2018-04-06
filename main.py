# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:17:37 2018

@author: wansho
"""
import tools
import os
import sex_classifier

# tools.parse_danmu()


############ 解析 xml 文件 获取弹幕 ##################
# 将xml文件中的弹幕解析出来，放到 train 文件夹中，只运行一次就好了
'''
config = 'notsex'

tools.parse_danmu(config)

config = 'sex'
tools.parse_danmu(config)
'''
#################################################
# 将要测试的弹幕xml文件放入 test文件夹中，然后开始检测

dirr_notsex = os.path.abspath('.') + '\\test'
files = os.listdir(dirr_notsex)

for file in files:
    print('-----------------------------')
    path = dirr_notsex + '\\' + file
    
    print(path)
    
    prob = sex_classifier.classifier(tools.parse_xml(tools.load_xml(path)) )
    if prob > 0.01: # 0.01 是训练得到的分界点
        print("软色情视频")
    else:
        print("不是软色情")









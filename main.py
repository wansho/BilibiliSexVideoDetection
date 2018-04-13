# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:17:37 2018

@author: wansho
"""
import tools
import os
import sex_classifier
import crawl

############ 解析 xml 文件 获取弹幕 用于训练 ##################
# 将xml文件中的弹幕解析出来，放到 train 文件夹中，只运行一次就好了
'''
config = 'notsex'

tools.parse_danmu(config)

config = 'sex'
tools.parse_danmu(config)
'''


#################################################
# 第一种测试方式： 将要测试的弹幕xml文件放入 test文件夹中，然后开始检测

def test1():
    dirr_notsex = os.path.abspath('.') + '\\test'
    files = os.listdir(dirr_notsex)
    
    for file in files:
        print('-----------------------------')
        path = dirr_notsex + '\\' + file
        
        print(path)
        
        result = sex_classifier.classifier(tools.parse_xml(tools.load_xml(path)) )
        if (result == 1 ):
            print("软色情视频")
        else:
            print("非软色情视频")
            
#################################################

# 第二种测试方式,直接输入av号，就能进行测试
            
def test2(av):
     
 
    comment_list = crawl.spider(str(av))
    
    if comment_list == -1:
        print('网页爬取失败')
    elif comment_list == '没有找到该视频':
        print('没有找到视频')
    else: # 开始分析是否为软色情视频
        result = sex_classifier.classifier(comment_list)
        if (result == 1 ):
            print("软色情视频")
        else:
            print("非软色情视频")
            
if __name__ == '__main__':
    # 输入av号：
    av = 4392812
    test2(av)
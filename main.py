# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:17:37 2018

@author: wansho
"""
import sex_classifier
import crawl

'''
更新软色情视频和正常视频的分界指数
'''
def update_divide_prob():
    sex_classifier.crawl_train_data()
    sex_classifier.train_classifier()
    pass

############ 根据av号进行测试 ##################
# 直接输入av号，就能进行测试       
def sex_test(av):
     
    danmu_list = crawl.spider(str(av))
    
    if danmu_list == -1:
        print('网页爬取失败')
    elif danmu_list == '没有找到该视频':
        print('没有找到视频')
    else: # 开始分析是否为软色情视频
        result = sex_classifier.classifier(danmu_list)
        if (result == 1 ):
            print("软色情视频")
        else:
            print("非软色情视频")
            
if __name__ == '__main__':
    # update_divide_prob()
    # 输入av号：
    av = 18436859
    sex_test(av)
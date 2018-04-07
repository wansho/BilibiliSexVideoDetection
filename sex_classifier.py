# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 15:16:23 2018

@author: wansho
"""
import os
import tools
import re

'''
分类器,只测试一个video的弹幕，返回该video是sex视频的概率
如果 > 0.01 就是软色情，如果 < 0.01 就不是软色情

如果要调整分类器的性能，就调整 sex_dict 字典中的特征即可
'''
def classifier(danmu_list):
    
    sex_dict = {'.*过审.*|.*营养.*跟不上.*|.*营养不良.*|.*看片.*|.*营养快线.*|.*身体被掏空.*|.*抽搐.*索然无味.*|.*可耻.*播放量.*': 6,
                    '.*打字.*清白.*|.*乳量.*|.*想日.*|.*观球.*|.*丝袜.*|.*石更.*|.*一硬.*|.*硬.*梆.*|.*梆.*硬.*|.*硬.*绑.*|.*绑.*硬.*|.*硬.*邦.*|.*邦.*硬.*' : 1
                    }
    score_sum = 0
    
    for danmu in danmu_list:
            
        score = 0
        regs = sex_dict.keys()
        for reg in regs:
            if len(re.findall(reg,danmu)) > 0:
                score = score + sex_dict.get(reg)
                
        score_sum= score_sum + score
    
    danmu_count = len(danmu_list)
    
    prob = score_sum / float(danmu_count)
    
    return prob

'''
显示训练集中每一个视频是软色情视频的概率，用来调整特征

最后得到的临界点是0.01， > 0.01 就是色情视频
'''
def show_sex_prob():
    
    print('--------------    sex    --------------')
    dirr_sex = os.path.abspath('.') + '\\train\\sex'
    files = os.listdir(dirr_sex) 
    
    for file in files:
        path = dirr_sex + '\\' + file
        video_danmu_list = tools.load_readlines(path)
        print(classifier(video_danmu_list))
        
    print('--------------  not sex  --------------')
    ######################### notsex ###############################

    dirr_notsex = os.path.abspath('.') + '\\train\\notsex'
    files = os.listdir(dirr_notsex)
    
    for file in files:
        path = dirr_notsex + '\\' + file
        video_danmu_list = tools.load_readlines(path)  
        print(classifier(video_danmu_list))

if __name__  == '__main__':
    show_sex_prob()
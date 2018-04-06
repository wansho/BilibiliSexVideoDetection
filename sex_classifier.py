# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 15:16:23 2018

@author: wansho
"""
import os
import tools
import re

'''
清理停用词
input:已经分词过的分词list
output: 不含有停用词的list
'''
def clear_chinese_stopwords(words):
    
    # 先加载停用词表
    stopwords_path = os.path.abspath('.') + '\\我的停用词.txt'
    
    stopwords  = []
    for word in tools.load_readlines(stopwords_path):
        stopwords.append(word.strip())
    
    # print(stopwords)
    nostopwords = []
    
    for word in words:
        if word.strip() not in stopwords:
            nostopwords.append(word.strip())

    return nostopwords

'''
词频统计，输入为词典，输出为两个数组，词频从高到低进行排序
'''
def word_frequency(dictt):
    word_list = []
    word_count = []
    
    for key in dictt.keys():
        word_list.append(key)
        word_count.append(dictt.get(key))
    
    # 开始排序
    j = len(word_list) -1
    while j > 0:
        i = 0
        while i < j:
            if word_count[i] < word_count[i + 1]:
                tmp = word_count[i]
                tmp1 = word_list[i]
                
                word_count[i] = word_count[i + 1]
                word_list[i] = word_list[i + 1]
                
                word_count[i + 1] = tmp
                word_list[i + 1] = tmp1
                
            i = i + 1
            
        j = j - 1
        
    return word_list,word_count



'''
分类器,只测试一个video的弹幕，返回该video是sex视频的概率

如果要调整分类器的性能，就调整 sex 字典中的特征即可
'''
def classifier(danmu_list):
    
    sex_dict = {'.*过审.*|.*营养.*跟不上.*|.*营养不良.*|.*看片.*|.*营养快线.*|.*身体被掏空.*|.*抽搐.*索然无味.*|.*可耻.*播放量.*': 6,
                    '.*打字.*清白.*|.*乳量.*|.*想日.*|.*观球.*|.*我添.*|.*丝袜.*|.*石更.*|.*一硬.*|.*硬.*梆.*|.*梆.*硬.*|.*硬.*绑.*|.*绑.*硬.*|.*硬.*邦.*|.*邦.*硬.*' : 1
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
获取sex弹幕的占比，训练得到的比例
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
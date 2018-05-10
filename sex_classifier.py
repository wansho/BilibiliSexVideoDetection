# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 15:16:23 2018

@author: wansho
"""
import os
import tools
import re
import crawl
import time
import random

'''
从 sex_av.txt 和 not_sex_av.txt 中加载av号
'''
def load_avs():
    sex_av_path = 'sex_av.txt'
    not_sex_av_path = 'not_sex_av.txt'
    
    fr_sex = open(sex_av_path,'r',encoding = 'utf-8')
    fr_not_sex = open(not_sex_av_path,'r',encoding = 'utf-8')
    
    sex_avs = set()
    not_sex_avs = set()
    
    for line in fr_sex:
        line = line.strip()
        sex_avs.add(line)
        
    for line in fr_not_sex:
        line = line.strip()
        not_sex_avs.add(line)
        
    return sex_avs, not_sex_avs

'''
从 sex_dict.txt 中加载色情词典（正则表达式）
'''
def load_sex_dict():
    
    sex_dict = {}
    score = -1
    path = 'sex_dict.txt'
    lines = tools.load_readlines(path)
    re_sex = ''
    for line in lines:
        line = line.strip()
        if line.startswith('score'):
            if score > 0:
                sex_dict[re_sex[1:]] = score
            score = int(line[line.index(':')+1:])
            re_sex = ''
        else:
            re_sex = re_sex + '|' + line
    sex_dict[re_sex[1:]] = score
    return sex_dict

'''
对每一个弹幕文件进行色情打分，得到非色情视频里面评分最高的，也就是色情程度最高的，
和色情视频里面评分最低的，也就是色情程度最低的，然后取两个评分的中值作为两种视频
的分界线,并存储该分界线。
'''
def train_classifier():
    
    print('--------------   sex  --------------')
    dirr_sex = os.path.abspath('.') + '\\train\\sex'
    files = os.listdir(dirr_sex)
    

    min_sex_prob = 1
    for file in files:
        path = dirr_sex + '\\' + file
        video_danmu_list = tools.load_readlines(path)
        prob = compute_sex_prob(video_danmu_list)
        if prob < min_sex_prob:
            min_sex_prob = prob
        print(path + '\n',prob)
      
    print('--------------  not sex  --------------')


    dirr_notsex = os.path.abspath('.') + '\\train\\notsex'
    files = os.listdir(dirr_notsex)
    
    max_notsex_prob = 0
    for file in files:
        path = dirr_notsex + '\\' + file
        video_danmu_list = tools.load_readlines(path)
        prob = compute_sex_prob(video_danmu_list)
        if prob > max_notsex_prob:
            max_notsex_prob = prob
        print(path + '\n' + str(prob))
    
    print("max_notsex_prob = " + str(max_notsex_prob))
    print("min_sex_prob = " + str(min_sex_prob)) 
    print((max_notsex_prob + min_sex_prob)/2)
    
    divide_prob = str((max_notsex_prob + min_sex_prob)/2)
    
    # 存储色情界限
    path = 'divide_prob.txt'
    fw = open(path, 'w', encoding = 'utf-8')
    fw.write(divide_prob)
    fw.flush()
    fw.close()

'''
根据输入的danmu list 打分
'''
def compute_sex_prob(danmu_list):
    sex_dict = load_sex_dict()
    
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
分类器,只测试一个video的弹幕，返回该video是sex视频的概率
如果 > 某个界限 就是软色情，如果 < 某个界限 就不是软色情

提高分类器的性能有两种方法：
    1、在 sex_dict.txt 中增加色情词，即色情特征词
    2、在 not_sex_av.txt 和 sex_av.txt中增加尽可能多的典型的av号
    3、完善色情正则表达式，防止误判

返回1 就是软色情视频
返回2 就是非软色情视频
'''
def classifier(danmu_list):
    
    # 加载 divide_prob
    path = 'divide_prob.txt'
    fr = open(path, 'r', encoding = 'utf-8')
    divide_prob = float(fr.read().strip())

    # 计算视频的色情指数
    prob = compute_sex_prob(danmu_list)
    
    if prob > divide_prob:
        return 1
    else:
        return 0

'''
爬取sex_av.txt 和 not_sex_av.txt中每条av的弹幕，并存储起来
'''
def crawl_train_data():
    
    sex_avs,not_sex_avs = load_avs()
    
    dirr_sex = os.path.abspath('.') + '\\train\\sex\\'
    dirr_notsex = os.path.abspath('.') + '\\train\\notsex\\'

    
    for sex_av in sex_avs:
        
        danmu_list = crawl.spider(str(sex_av))
        if danmu_list == -1:
            print('网页爬取失败')
        elif danmu_list == '没有找到该视频':
            print('没有找到视频')
            continue
        else: # 开始给色情词打分
            classifier(danmu_list)# 打印出该视频的色情得分
            path = dirr_sex + sex_av + '.txt'
            tools.write_danmu(path,danmu_list)
            time.sleep(random.randint(3,5))
        
    for not_sex_av in not_sex_avs:
        
        danmu_list = crawl.spider(str(not_sex_av))
        if danmu_list == -1:
            print('网页爬取失败')
        elif danmu_list == '没有找到该视频':
            print('没有找到视频')
            continue
        else: # 开始给色情词打分
            classifier(danmu_list)# 打印出该视频的色情得分
            path = dirr_notsex + not_sex_av + '.txt'
            tools.write_danmu(path,danmu_list)
            time.sleep(random.randint(3,5))

if __name__  == '__main__':
    
    pass
    # crawl_train_data()
    # train_classifier()
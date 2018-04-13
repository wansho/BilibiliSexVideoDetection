# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:54:38 2018

爬取到xml文件

@author: wansho
"""

from lxml import etree
import requests
import re
from bs4 import BeautifulSoup



def downloadHtml(url,headers):
   
    html = -1 # 如果返回 -1，说明爬取失败
      
    try:
        html = requests.get(url, headers=headers).text
    except Exception as e:
        print(e)
        return html
    return html

'''
用beautifulsoap 修补一下网页，并存储，用来研究
'''
def fix_and_write_html(html_str,path):
    # 修补html
    soup = BeautifulSoup(html_str,'html.parser',from_encoding="gb18030")
    fixed_html = soup.prettify()
    
    writer = open(path, 'w',  encoding='utf-8')
    writer.write(fixed_html)
    writer.close()
    
    return fixed_html



def spider(av):
    
    headers = { 
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Language':'zh-CN,zh;q=0.9',
		 'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':'finger=edc6ecda; fts=1523587270; LIVE_BUVID=AUTO5215235872705182; UM_distinctid=162bce0cac47eb-0cc36799bfd956-b34356b-13c680-162bce0cac5579; pgv_pvi=2245154816; pgv_si=s1499492352; buvid3=A0C350F4-B5D7-491C-AE37-4CE057958C30140264infoc; sid=d2tsk007; rpdid=lqmwxowwqdosiksqmkiw; DedeUserID=72195837; DedeUserID__ckMd5=ce6e1cb27593719c; SESSDATA=c85de437%2C1526180883%2Cbd52000b; bili_jct=e9f83985c638c1f18b2fadf44f67096c; _dfcaptcha=733d11abcdeaf6dd73d53c489d31ad0a; CNZZDATA2724999=cnzz_eid%3D865291217-1523583696-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1523594496',
        'Host':'www.bilibili.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'    
	} 
    
    cid = '没有找到该视频'
    
    url = 'https://www.bilibili.com/video/av' + av + '/'
    html = downloadHtml(url,headers)
    
    if html == -1:
        print('网页爬取失败')
        return html
    
    soup = BeautifulSoup(html)
    cid_soup = soup.find('input',attrs = {'id' : 'link2', 'type' : 'text'})
    
    if cid_soup == None:
        return cid   
    
    cid_str = cid_soup.get('value')
    
    re_cid = 'cid=[0-9]+'
    cid = re.findall(re_cid,cid_str)[0][4:]
    
    comment_url = 'https://comment.bilibili.com/' + cid + '.xml'

    
    '''
    xml的header和视频页的header不一样，需要重新构造（小写字母，不需要长连接），否则会被反爬虫拦截
    ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
    '''
    xml_header = { 
		'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'accept-language':'zh-CN,zh;q=0.9',
		'cache-control':'max-age=0',
		'cookie':'finger=edc6ecda; fts=1523587270; LIVE_BUVID=AUTO5215235872705182; UM_distinctid=162bce0cac47eb-0cc36799bfd956-b34356b-13c680-162bce0cac5579; pgv_pvi=2245154816; pgv_si=s1499492352; buvid3=A0C350F4-B5D7-491C-AE37-4CE057958C30140264infoc; sid=d2tsk007; rpdid=lqmwxowwqdosiksqmkiw; DedeUserID=72195837; DedeUserID__ckMd5=ce6e1cb27593719c; SESSDATA=c85de437%2C1526180883%2Cbd52000b; bili_jct=e9f83985c638c1f18b2fadf44f67096c; _dfcaptcha=733d11abcdeaf6dd73d53c489d31ad0a; CNZZDATA2724999=cnzz_eid%3D865291217-1523583696-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1523594496',
		'upgrade-insecure-requests':'1',
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'    
	}  
    
    comment_text = requests.get(comment_url, headers=xml_header).content
    
    comment_selector = etree.HTML(comment_text)
    comment_content = comment_selector.xpath('//i')
    comment_list = []
    for comment_each in comment_content:
        comments = comment_each.xpath('//d/text()')
        for comment in comments:
            comment_list.append(comment)
    
    return comment_list

if __name__ == '__main__':
    pass
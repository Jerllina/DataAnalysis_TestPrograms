# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 17:15:59 2018

@author: Jelina
"""

import requests
from bs4 import BeautifulSoup
import csv

##数据获取模块 
#下载网页 通用模块
def download(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1;Win64;x64)AppleWebKit/537.36 (KHTML,like Gecko) Chrome/59.0.3071.115 Safari/537.36' }
    response=requests.get(url,headers=headers)
    #print(response.status_code)
    return response.text
    
 #数据采集 
 #解析所需要的数据列表信息 包含表头
 #获取主网页公司数据列表信息 
rank_list=[]

def get_content_first_page(html,country='China'):
    soup=BeautifulSoup(html,'lxml')
    body=soup.body
    body_content=body.find('div',{'class':'content post'})
    tables=body_content.find_all('table')
    # tables一共有2个，取第一个
    trs = tables[0].find_all('tr')
    #获取表头名称
    #trs[1] 和其他年份不同
    row_title=[item.text for item in trs[0].find_all('td')]
    row_title.insert(2, 'Country')
    
    rank_list.append(row_title)
    for i,tr in enumerate(trs):
         if i == 0:
             continue
         tds=tr.find_all('td')        
         #获取公司排名和列表
         row = [item.text.strip() for item in tds]
         row.insert(2,country)
         rank_list.append(row)
    return rank_list

#获取主页面的其他页面链接 （其他国家名称
def get_country_info(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    label_div = body.find('div', {'class':'content post'})
    tables=label_div.find_all('table')
    
    label_a = tables[1].find_all('a')
    country_names = [item.text for item in label_a]
    page_urls = [item.get('href') for item in label_a]
    country_info=list(zip(country_names,page_urls))
    return country_info

#获取分页面的数据列表信息
def get_content_other_page(html,country):
    soup=BeautifulSoup(html,'lxml')
    body=soup.body
    body_content=body.find('div',{'class':'content post'})
    tables=body_content.find_all('table')
    # tables一共有2个，取第一个
    trs = tables[0].find_all('tr')
       
    for i,tr in enumerate(trs):
         if i == 0:
             continue
         tds=tr.find_all('td')
         
         #获取公司排名和列表
         row = [item.text.strip() for item in tds]
         row.insert(2,country)
         rank_list.append(row)    
    
    return rank_list 


#数据存储模块  .csv格式      
def save_data_to_csv_file(data, file_name):
    with open(file_name,'a',errors='ignore',newline='')as f:
        f_csv=csv.writer(f)
        f_csv.writerows(data)
        

#数据采集主函数模块
def get_forbes_global_year_2013():
    url='http://www.economywatch.com/companies/forbes-list/china.html'
    html=download(url)
    #print(html)
    
    data_first_page=get_content_first_page(html)
    #print(data_first_page)
    save_data_to_csv_file(data_first_page,'forbes_economywatch_2013.csv')
    print('saving data ...', 'China')
    
    country_info=get_country_info(html)
    #print(country_info)
    
    
    for item in country_info:
        country_name=item[0]
        country_url=item[1]
        if country_name=='China':
            continue
        html=download(country_url)
        data_other_country=get_content_other_page(html,country_name)
        print('saving data...',country_name)
        save_data_to_csv_file(data_other_country,'forbes_economywatch_2013.csv' )

if __name__=='__main__' :

    get_forbes_global_year_2013() 
    print('(●· 。·●) Good job!you download all data successfully!')

 
    

    
         
    
    
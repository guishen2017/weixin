#-*- coding:utf-8 -*-
import requests
import json
import re
import random
import time
import pymongo
from conf import *

client = pymongo.MongoClient(host="127.0.0.1")
db = client['weixin']
table = db['article_detail']

weixin_cooike = None
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
}
def get_cookie():
    with open('cookie.txt','r',encoding='utf-8') as f:
        cooike = f.read()
        global weixin_cooike
        weixin_cooike = json.loads(cooike)

def get_article(name):
    response = requests.get(url = "https://mp.weixin.qq.com",headers = headers,cookies = weixin_cooike)
    token = get_token(response.url)
    searchbiz_data = {
        'action':'search_biz',
        'ajax':'1',
        'begin':'0',
        'count':'5',
        'f':'json',
        'lang':'zh_CN',
        'query':name,
        'random':random.random(),
        'token':token
    }
    searchbiz_response = requests.get('https://mp.weixin.qq.com/cgi-bin/searchbiz',params=searchbiz_data, headers = headers,cookies = weixin_cooike)
    searchbiz_json = json.loads(searchbiz_response.text)
    fakeid = searchbiz_json['list'][0]['fakeid']
    appmsg_data = {
        'action':'list_ex',
        'ajax':'1',
        'begin':'0',
        'count':'5',
        'f':'json',
        'fakeid':fakeid,
        'lang':'zh_CN',
        'query':'',
        'random':random.random(),
        'token':token,
        'type':'9',
    }
    appmsg_response = requests.get("https://mp.weixin.qq.com/cgi-bin/appmsg", params=appmsg_data,headers = headers,cookies = weixin_cooike)
    appmsg_json = json.loads(appmsg_response.text)
    article_count = int(appmsg_json['app_msg_cnt'])
    num = round(article_count/5)
    for n in range(0,num+1):
        appmsg_data['begin'] = str(n*5)
        appmsg_response = requests.get("https://mp.weixin.qq.com/cgi-bin/appmsg", params=appmsg_data, headers=headers,cookies=weixin_cooike)
        appmsg_json = json.loads(appmsg_response.text)
        for data in appmsg_json['app_msg_list']:
            detail_url = data['link']
            title = data['title']
            print(detail_url)
            print(title)
            save_to_mongodb(name,detail_url,title)
        time.sleep(5)


def save_to_mongodb(name, detail_url, title):
    article = {
        'name':name,
        'detail_url':detail_url,
        'title':title,
    }
    table.insert(article)

def get_token(url):
    regex = re.compile(r"token=(\d+)")
    token = regex.findall(url)[0]
    return token

if __name__ == "__main__":
    get_cookie()
    get_article(search_keys)

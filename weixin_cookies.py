#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conf import *
import time
import json

chrome = webdriver.Chrome()
wait = WebDriverWait(chrome, 10)
cookie = {}

def login_weixin():

    login_url = "https://mp.weixin.qq.com/"
    chrome.get(login_url)
    user_name = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="account"]')))
    user_name.clear()
    user_name.send_keys(username)
    password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
    password.clear()
    password.send_keys(pwd)
    remember = wait.until(EC.presence_of_element_located((By.XPATH, '//i[@class="icon_checkbox"]')))
    remember .click()
    login = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@title="点击登录"]')))
    login .click()
    time.sleep(20)
    get_cookie()

def get_cookie():
    cookies = chrome.get_cookies()
    print(cookies)
    global cookie
    for c in cookies:
        print("name:%s,value:%s."%(c['name'],c['value']))
        cookie[c['name']] = c['value']
    print(cookie)
    with open('cookie.txt', "w", encoding='utf-8') as f:
        f.write(json.dumps(cookie))
    chrome.close()

login_weixin()

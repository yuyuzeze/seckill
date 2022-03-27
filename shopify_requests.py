# -*- coding: UTF-8 -*-
from session import SpiderSession
from bs4 import BeautifulSoup
from logger import logger
#from urllib.parse import urlparse
from util import (
    send_wechat,
    wait_some_time
)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import requests
import time
import warnings
warnings.filterwarnings("ignore")

global keywords
keywords = ['']

class Monitor(object):
    def __init__(self):
        # 数据结构 
        # [0][0] 名称
        #    [1] URL
        #    [2] 数组[{商品名，链接}]
        self.category = [] 
        self.spider_session = SpiderSession()
        self.spider_session.load_cookies_from_local()

        self.session = self.spider_session.get_session()
        self.user_agent = self.spider_session.user_agent
        
    def scrape_category(self, index):
        items = []

        url = self.category[index][1]
        headers = {
            'User-Agent': self.user_agent
        }   
        html = self.session.get(url=url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(html.text, 'html.parser')
        array = soup.find_all('div', {'class': 'item__container'})

        # 遍历左边的分类
        for i in array:
            item = [i.find('span', {'class': 'item__name'}).text,
                    i.find('a')['href']]
            items.append(item) 

        if(self.category[index][2] != items):
            diffs = [x for x in items if x not in self.category[index][2]]
            msg = ''
            for j in diffs:
                for k in keywords:
                    if k in j[0]:
                        msg += '[{}]({})\r\r'.format(j[0],j[1])
                        continue
            #第一次不提醒        
            if(len(self.category[index][2]) > 0 and msg != ''):
                print("Got'It!")
                send_wechat(self.category[index][0].replace("'",""), msg)
            self.category[index][2] = items

        print(time.strftime('%Y-%m-%d %X %p'))

    def make_scrape(self):
        items = []

        url = ''
        headers = {
            'User-Agent': self.user_agent
        }
        html = self.session.get(url=url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(html.text, 'html.parser')
        array = soup.find_all('li', {'class': 'accordion'})

        # 遍历左边的分类
        for i in array:
            if(i.find('span', {'class': 'drawer-nav-list__name'}) != None):
                item = [i.find('span', {'class': 'drawer-nav-list__name'}).text,
                        i.find('a')['href'],[]]
                items.append(item)

        if(len(self.category) != len(items)):
            diffs = [x for x in items if x not in self.category]
            msg = ''
            for j in diffs:
                msg += '[{}]({})\r\r'.format(j[0],j[1])
            self.category = items

        #主要监控 TODAY'S NEW!
        for k in range(len(self.category)):
            if "TODAY" not in self.category[k][0]: 
                continue   
            self.scrape_category(k)

    def scrape(self):
        while True:
            try:
                self.make_scrape()
            except Exception as e:
                logger.info('监控异常!', e)
            wait_some_time()

class SecKill(object):       
      
    def seckill(self):
        driver = self.driver
        for key in keywords:
            try:                
               eles = driver.find_elements_by_xpath('//*[@id="main_middle"]/div/div/div/div/a/span[contains(text(), "' + key + '")]/..')
               for ele in eles:
                   soldout = ele.find_elements_by_class_name('icon-product-tag')
                   isbear = ele.find_elements_by_xpath('//span[contains(text(), "クマ")]')
                   if(len(soldout) == 0 and len(isbear) == 0):
                        ele.click()
            except:
                print()       

    def seckill_by_selenium(self):
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get('')
        self.driver = driver
        self.count = 0
        time.sleep(1)

        key = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="drawer-toggle"]')))
        key.click()
        time.sleep(1)

        key = WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="drawer-nav"]//span[contains(text(), "TODAY")]/..')))
        key.click()
        time.sleep(1)

        url = driver.current_url

        while True:
            try:
                self.seckill()
            except Exception as e:
                logger.info('抢购异常!', e)
            
            if(self.count == 1):
                print("结束")
                return

            driver.get(url)
            wait_some_time() 



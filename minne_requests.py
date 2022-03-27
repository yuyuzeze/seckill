# -*- coding: UTF-8 -*-
from urllib import request
from session import SpiderSession
from bs4 import BeautifulSoup
from logger import logger
from urllib.parse import urlparse
from util import (
    send_wechat,
    wait_some_time
)
from selenium import webdriver

import requests
import time

class Monitor(object):
    def __init__(self):
        self.category = []
        self.spider_session = SpiderSession()
        self.spider_session.load_cookies_from_local()

        self.session = self.spider_session.get_session()
        self.user_agent = self.spider_session.user_agent

    def make_scrape(self):
        url = 'https://minne.com/@orange-t-e-a?keywords=&mode=saleonly&page=1&per_page=20&sort=position/'
        headers = {
            'User-Agent': self.user_agent
        }
        html = self.session.get(url=url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(html.text, 'html.parser')
        array = soup.find_all('div', {'class': 'galleryProductList__item'})
        
        # 遍历左边的分类
        for i in array:
            if(i.find('a', {'class': 'js-product-list-click-tracking'}) != None):
                send_wechat("minne")
        #print(msg)

    def scrape(self):
        while True:
            try:
                self.make_scrape()
            except Exception as e:
                logger.info('监控异常!', e)
            wait_some_time()
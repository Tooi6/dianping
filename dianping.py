# -*- coding:utf-8 -*-

"""
Updated at 10:40 at April 25,2019
@title: 花式反爬之大众点评
@author: Northxw
"""

import requests
import urllib.error
import numpy as np
from scrapy.selector import Selector
from proxy import xdaili_proxy, general_proxy
from config import *
from parse import parse
from pymongo import MongoClient
from utils.common import *
import time
import re
import os
import json
from fontTools.ttLib import TTFont
from utils.ParseFont import ParseFontClass


class Dianping(object):
    def __init__(self):
        self.headers = HEADERS
        self.proxies = xdaili_proxy()
        self.cookie = COOKIES
        self.css_url = CSS_URL
        self.svg_num_url = SVG_NUM_URL
        self.svg_font_url = SVG_FONT_URL
        self.client = MongoClient(MONGO_CLIENT)
        self.db = self.client.dianping
        self.collection = self.db.shop
        # 字体工具
        self.parseFont = ParseFontClass(proxies=self.proxies, headers=self.headers)

    def get_store_list_page(self, url):
        try:
            # print(self.proxies)
            response = requests.get(url, headers=self.headers, proxies=self.proxies,
                                    cookies=self.cookie)
            if response.status_code == 200:
                return response
        except urllib.error.HTTPError as e:
            print(e.reason)

    def parse_data(self, response):
        res = Selector(text=response.text)
        try:
            li_list = res.xpath('//*[contains(@class, "shop-all-list")]/ul/li')
            if li_list:
                for li in li_list:
                    data = parse(li, self.parseFont, self.svg_num_url, self.svg_font_url, self.css_url)
                    # print(data)
                    self.save_to_db(data)
                    # break
        except Exception as e:
            print('Error: %s, Please Check it.' % e.args)

    def save_to_db(self, data):
        self.collection.insert_one(data)

    def load_tff(self, response):
        res = Selector(text=response.text)
        # 加载css文件
        css_list = res.xpath('//*[contains(@type, "text/css")]/@href')
        css_list = get_font_css(css_list.extract())
        for css in css_list:
            self.parseFont.get_ttf(css_url="http:" + css)

    def main(self):
        """
        主函数
        """
        for i in range(10):
            # for i in tqdm(range(10), desc='Grabbing', ncols=100):
            print("第%d页：" % (i + 1))

            # 请求商铺页面列表
            response = self.get_store_list_page(INIT_URL.format(str(i + 1)))
            if response.url.find('verify') > -1:
                print("反爬验证！")
                continue
            # 加载字库
            self.load_tff(response)
            # 解析数据
            self.parse_data(response)
            time.sleep(np.random.randint(1, 3))
            # 测试仅抓取第一页
            # break


if __name__ == '__main__':
    dianping = Dianping()
    dianping.main()

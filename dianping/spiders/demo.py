import scrapy
from scrapy.http import Request
from dianping.items import DianpingItem
from utils.ParseFont import ParseFontClass
import re


class mingyan(scrapy.Spider):  # 需要继承scrapy.Spider类
    name = "demo"  # 定义蜘蛛名
    allowed_domains = ['www.dianping.com']
    first_url = 'http://www.dianping.com/shenzhen/ch10/g114'
    last_url = 'p'

    def start_requests(self):
        for i in range(1, 2):
            url = self.first_url + self.last_url + str(i)
            yield Request(url, self.parse)

    def parse(self, response):
        # 加载字体
        css = response.xpath('/html/head/link[@type="text/css"]/@href')
        pf = self.loadFont(css=css)

        shops = response.xpath('//*[@id="shop-all-list"]/ul/li')
        for shop in shops:
            item = DianpingItem()
            try:
                item['name'] = shop.xpath('./div[2]/div[1]/a[1]/h4//text()').extract()[0]
                item['location'] = shop.xpath(
                    './div[@class="operate J_operate Hide"]/a[@class="o-map J_o-map"]/@data-address').extract()[0]
                yield item
            except:
                pass

    def loadFont(self, css):
        pf = None
        for str in css.extract():
            if str.find('svgtextcss') > 0:
                pf = ParseFontClass('http://' + str)
        return pf

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class DianpingPipeline(object):  # 设置工序一
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['店铺名称', '地点',])

    def process_item(self, item, spider):
        line = [item['name'], item['location']]  # 把数据中每一项整理出来
        self.ws.append(line)
        self.wb.save('dianping.xlsx')  # 保持xlsx文件
        return item

    def spider_closed(self, spider):
        self.file.close()

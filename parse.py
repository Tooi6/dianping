# -*- coding:utf-8 -*-

import re
from config import *
import requests
from utils.common import get_md5


def parse(li, parseFont, svg_num_url, svg_font_url, css_url):
    """
    解析数据
    """
    data = dict()
    # 店铺名称
    data['name'] = li.css('.txt .tit > a > h4::text').extract_first(DEFAULT_NAME)
    # 店铺封面
    data['img'] = li.css('.pic > a > img::attr(src)').extract_first('').split('%')[0]
    # 店铺链接
    data['shop_detail_url'] = li.css('.txt .tit > a:nth-child(1)::attr(href)').extract_first('')
    # ID
    data['id'] = get_md5(data['shop_detail_url'])
    # 星级
    # data['star'] = li.css('.txt .comment > span::attr(title)').extract_first(DEFAULT_STAR)
    # 评论数
    # comment_inner_number = li.css('.txt .comment > a.review-num > b::text').extract_first()
    # comment_class_list = re.findall(r'class="(.*?)">', li.css('.txt .comment > a.review-num > b').extract_first(), re.S)
    # data['comments'] = comment_inner_number + get_completed_nums(svg_num_url, css_url, comment_class_list)
    comment_html = li.css('.txt .comment > a.review-num > b').extract_first()
    comment_codes = re.findall(r'>(.*?)<', comment_html, re.S)
    data['comments'] = handle_nums(parseFont, comment_codes)

    # 人均价
    price_html = li.css('.txt .comment > a.mean-price > b').extract_first()
    price_code = re.findall(r'>(.*?)<', price_html, re.S)
    data['price'] = handle_nums(parseFont, price_code)
    # 口味
    taste_html = li.xpath('div[2]/span/span[1]/b').extract_first('')
    taste_code = re.findall(r'>(.*?)<', taste_html, re.S)
    data['taste'] = handle_nums(parseFont, taste_code)
    # 环境
    environment_html = li.xpath('div[2]/span/span[2]/b').extract_first('')
    environment_code = re.findall(r'>(.*?)<', environment_html, re.S)
    data['environment'] = handle_nums(parseFont, environment_code)
    # 服务
    quality_html = li.xpath('div[2]/span/span[3]/b').extract_first('')
    quality_code = re.findall(r'>(.*?)<', quality_html, re.S)
    data['quality'] = handle_nums(parseFont, quality_code)

    # # 美食分类
    # type_class_list = re.findall(r'class="(.*?)">', li.css('.txt .tag-addr > a:nth-child(1) > span').extract_first(), re.S)[1:]
    # data['food_type'] = get_completed_font_424(svg_font_url, css_url, type_class_list)
    # # 地址
    # address_class_list = re.findall(r'class="(.*?)">', li.css('.txt .tag-addr > a:nth-child(3) > span').extract_first(), re.S)[1:]
    # data['fuzzy_address'] = get_completed_font_424(svg_font_url, css_url, address_class_list)
    # print(data['fuzzy_address'])
    # # 详细地址
    # detail_address_class_list = re.findall(r'class="(.*?)">', li.css('.txt > div.tag-addr > span').extract_first(), re.S)[1:]
    # data['detail_address'] = get_completed_font_424(svg_font_url, css_url, detail_address_class_list)
    # print(data['detail_address'])

    # 美食分类
    type_html = li.css('.txt .tag-addr > a:nth-child(1) > span').extract_first()
    type_code = re.findall(r'>(.*?)<', type_html, re.S)
    data['food_type'] = handle_nums(parseFont, type_code)
    # 地址
    address_html = li.css('.txt .tag-addr > a:nth-child(3) > span').extract_first()
    address_code = re.findall(r'>(.*?)<', address_html, re.S)
    data['fuzzy_address'] = handle_nums(parseFont, address_code)
    # # 详细地址
    # detail_address_class_list = re.findall(r'class="(.*?)">', li.css('.txt > div.tag-addr > span').extract_first(), re.S)[1:]
    # data['detail_address'] = get_completed_font_425(svg_font_url, css_url, detail_address_class_list)
    # print(data['detail_address'])
    # 推荐菜
    # data['recommend'] = '|'.join(re.findall('blank.*?>(.*?)</a>', li.css('.txt .recommend').extract()[0], re.S))
    return data


def handle_nums(parseFont, codes):
    num = ''
    for code in codes:
        # code转unicode
        unicode = code.encode('unicode_escape')
        if unicode.startswith(b'\ue') or unicode.startswith(b'\uf'):
            # 提取字体编码
            temp = str(unicode).replace('\'', '')[-4:]
            # 解析
            temp = parseFont.parse_ttf(temp)
            if temp != False:
                code = temp
        num = num + code
    return num


def get_completed_nums(svg_num_url, css_url, class_list):
    """
    处理数字
    """
    completed_nums = ''
    result_svg = requests.get(svg_num_url).text
    # svg页面源码中text标签内的文本值
    a, b, c = re.findall('y=.*?>(.*?)<', result_svg, re.S)
    # text标签内的y属性值
    y1, y2, y3 = re.findall('y="(.*?)">', result_svg, re.S)
    # 字体大小
    divisor = eval(re.search('x="(\d{2}) ', result_svg, re.S).group(1))
    for class_ in class_list:
        x, y = get_coordinate_value(css_url, class_)
        x, y = int(x), int(y)
        if y < int(y1):
            completed_nums += a[x // divisor]
        elif y < int(y2):
            completed_nums += b[x // divisor]
        elif y < int(y3):
            completed_nums += c[x // divisor]
    return completed_nums


def get_completed_font_424(svg_font_url, css_url, class_list):
    """
    处理文字
    - 2019/4/24 测试期间规律：svg源码中通过class属性的y坐标确定text所在行的id值，然后text[x//divisor]获取正常字符
    """
    # 完整字符串
    completed_font = ''
    # 剔除 <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    svg_font_text = re.sub('<\?xml.*?\?>', '', requests.get(svg_font_url).text)
    # 获取id、d属性值组成的元组
    path_list = re.findall('id="(\d+)"\sd="M0\s(\d+)\sH600"', svg_font_text, re.S)
    # 获取href、text值组成的元组
    textpath_list = re.findall('href="#(\d+)".*?>(.*?)<', svg_font_text, re.S)
    # 字体大小
    divisor = eval(re.findall('font-size:(\d+)px', svg_font_text, re.S)[0])
    for class_ in class_list:
        # class对应坐标值
        x, y = get_coordinate_value(css_url, class_)
        x, y = int(x), int(y)
        # 确定当前class的id值
        class_id_location = [tup[0] for tup in path_list if y < int(tup[-1])][0]
        # 根据id值确定文字所在字符串
        class_id_text = [tup[-1] for tup in textpath_list if tup[0] == class_id_location][0]
        # 根据偏移量获取最终需要的文字
        target_text = class_id_text[x // divisor]
        completed_font += target_text
    return completed_font


def get_completed_font_425(svg_font_url, css_url, class_list):
    """
    处理文字
    - 2019/4/25 测试期间规律：svg源码中通过y确定偏移字体所在文本行, 然后通过text[x//divisor]获取正常字符
    """
    completed_font = ''
    svg_font_text = re.sub('<\?xml.*?\?>', '', requests.get(svg_font_url).text)
    # 获取y、text值组成的元组列表
    y_text_list = re.findall('y="(.*?)">(.*?)<', svg_font_text, re.S)
    divisor = eval(re.search('font-size:(\d+)px', svg_font_text, re.S).group(1))
    for class_ in class_list:
        # class对应坐标值
        x, y = get_coordinate_value(css_url, class_)
        x, y = int(x), int(y)
        # 获取当前class对应文字所在文本行
        class_text = [tup[-1] for tup in y_text_list if y < int(tup[0])][0]
        # 根据偏移量获取最终需要的文字
        target_text = class_text[x // divisor]
        completed_font += target_text
    return completed_font


def get_coordinate_value(css_url, class_):
    """
    处理class, 获取坐标值
    """
    css_html = requests.get(css_url).text
    info_css = re.findall(r'%s{background:-(\d+).0px -(\d+).0px' % class_, css_html, re.S)[0]
    return info_css


if __name__ == '__main__':
    pass
    # get_completed_font(CSS_URL, SVG_FONT_URL, ['jv3j8', 'jvu8v', 'jvp6e', 'jv8vh'])

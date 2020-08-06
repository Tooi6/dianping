# -*- coding:utf-8 -*-

from fake_useragent import UserAgent
import random

API = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=6572f9ab6d5d49deb807779f4f13b774&orderno=YZ2020863778MEgdEc&returnType=2&count=1'

INIT_URL = 'http://www.dianping.com/beijing/ch10/p{}'
CSS_URL = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/f8198800680006c0424b3c7412023ee7.css'
SVG_NUM_URL = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/20b501902c483d49e1e66d2159f1d2b8.svg'
SVG_FONT_URL = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/37b6ad50c87b9ec0e1744f4291efb622.svg'

MAX_PAGES = 20

# 获取随机UA
with open('./utils/ua.log', 'r', encoding='utf-8') as f:
    random_ua = random.choice(f.read().split('\n'))

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/beijing/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random_ua,
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    # "Proxy-Tunnel": str(random.randint(1,10000))  # 使用亿牛云代理时需设置
}

# COOKIES = ''
COOKIES = 's_ViewType=10; _lxsdk_cuid=173bde0b72ec8-00e1c25a6bbe9d-c343162-1fa400-173bde0b72ec8; _lxsdk=173bde0b72ec8-00e1c25a6bbe9d-c343162-1fa400-173bde0b72ec8; _hc.v=f18c28f2-8fde-c250-c4c9-ecf75eae19cb.1596618488; fspop=test; cy=247; cye=nanchong; dper=1bfc18ec56948893d36a76803557e26b5078c03e319b351032ab2428007ba4b995d96a263905089b35279cff64a15b3feca2f6c2897558bc6fdaf5318224773f6b5be40b3f5cba45dfd2fd4d229a245da1b05fc7d2d1c17860bd7df7f53ecc49; ua=QI_611122484; ctu=cc0ce4f2d9cb25849c6477eeeecaa14e3caf7d051ffabe62f5105af2e003a5c4; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1596622469,1596676237,1596679566,1596680624; dplet=06d4f75186ee07af91c8d61dd82af671; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1596698974; _lxsdk_s=173c2a8c679-fc7-5c3-860%7C%7C61'
COOKIES = {cookie.split('=')[0]: cookie.split('=')[1]
           for cookie in COOKIES.replace(' ', '').split(';')}

# 阿布云
PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"
PROXY_USER = 'HL3E438N64G79I6D'
PROXY_PASS = 'C54E0F0C2E3EC0DE'

# 亿牛云
NIU_PROXY_HOST = 'p5.t.16yun.cn'
NIU_PROXY_PORT = '6445'
NIU_PROXY_USER = 'SASDV58VF'
NIU_PROXY_PASS = 'Vf5v21vF'

DEFAULT_STAR = '三星级商户'
DEFAULT_NAME = 'Unnamed'
DEFAULT_NUM = 10

MONGO_CLIENT = 'mongodb://root:123456@192.168.142.135:27017/admin?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'

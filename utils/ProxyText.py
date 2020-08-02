import requests
#测试付费代理和加密代理
url = 'http://httpbin.org/get'

proxy_host = 'http-dyn.abuyun.com'
proxy_port = '9020'

proxy_user = 'HL3E438N64G79I6D'
proxy_pass = 'C54E0F0C2E3EC0DE'

proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
    'host': proxy_host,
    'port': proxy_port,
    'user': proxy_user,
    'pass': proxy_pass,
}

proxies = {
    'http': proxy_meta,
    'https': proxy_meta,
}

response = requests.get(url, proxies=proxies)
print(response.text)
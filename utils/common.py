import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_font_css(css_list):
    """过滤字体css"""
    result = []
    for css in css_list:
        if (css.find('svgtextcss')) > 0:
            result.append(css)
    return result


@staticmethod
def get_ttf_urls(text):
    """提取字体链接"""
    ttf_urls = []
    urls = re.findall(r'url\("//(.*?)"\)', text)
    for url in urls:
        if url not in ttf_urls and '.woff' in url:
            ttf_urls.append(url)

    return ttf_urls


if __name__ == '__main__':
    pass

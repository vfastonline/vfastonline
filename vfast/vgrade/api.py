#!encoding:utf-8
from vgrade.models import Headimg

#返回所有头像图片的URL
def headimg_urls():
    """返回系统图片保存位置列表
    [u'/static/head/tuzi.jpg', u'/static/head/shitou.jpg']
    """
    urls = []
    results = Headimg.objects.filter(type=1).values('url')
    for url in results:
        urls.append(url['url'])
    return urls
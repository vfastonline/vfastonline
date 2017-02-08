#!encoding:utf-8
from vgrade.models import Headimg

#返回所有头像图片的URL
def headimg_urls():
    urls = Headimg.objects.filter(type=1).values('url')[0]
    return urls
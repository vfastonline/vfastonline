#!encoding:utf-8
from django import template
import time
register = template.Library()


@register.filter
def get_list_index(list, index):
    return list[index+1]


@register.filter(name='hello')
def hello(value):
    return value +' aa  dapeng'


@register.filter(name='get_next_lession_url')
def get_next_lession_url(list, index):
    try:
        video = list[index+1]
        if video['vtype'] == 0:
            return '/video/%s' % video['id']
        else:
            return '/practice/%s' % video['id']
    except:
        return

@register.filter(name='dashboard_get_lession_url')
def dashboard_get_lession_url(list):
    if list['vtype'] == 0:
        return '/video/%s' % list['video_id']
    else:
        return '/practice/%s' % list['video_id']


def time_To_unixtime(str):
    """2015-09-08 10:10:10 时间转换成为时间戳"""
    t = time.mktime(time.strptime(str, '%Y-%m-%d %H:%M:%S'))
    return int(t)


@register.filter(name='time_comp_now')
def time_comp_now(str):
    """时间与当前时间比较,转换为几分钟前, 几小时前, 几天前, 几月前, 时间"""
    now = int(time.time())
    interval = now - time_To_unixtime(str)
    # print interval
    if interval < 60:
        return '%s秒前' % interval
    elif interval / 60 < 60:
        return '%s分钟前' % (interval / 60)
    elif interval / 60 / 60 < 24:
        return '%s小时前' % (interval / 60 / 60)
    elif interval / 60 / 60 / 24 < 30:
        return '%s天前' % (interval / 60 / 60 / 24)
    elif interval / 60 / 60 / 24 / 30 < 5:
        return '%s月前' % (interval / 60 / 60 / 24 / 30)
    else:
        return interval


@register.filter(name='secTomin')
def secTomin(str):
    """观看时间秒转化成为分钟, 小时"""
    second = int(str)
    return int(second / 60)

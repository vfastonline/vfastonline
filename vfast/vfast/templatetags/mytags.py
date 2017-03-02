#!encoding:utf-8
from django import template


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

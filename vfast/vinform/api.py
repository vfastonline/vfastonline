#!/usr/bin/env python
#encoding:utf-8
from vfast.api import dictfetchall, second_to_hour
from vcourse.models import Video

def get_score_yesterday(uid, yesterday):
    """获取昨日总得分"""
    sql = "select sum(score) as score from vrecord_score where createtime='%s' and user_id=%s;" % (yesterday, uid)
    result = dictfetchall(sql)
    score = result[0]['score'] if result[0]['score'] else 0
    return score


def get_videotime_yesterday(uid,yesterday):
    """获取昨日观看视频总时长"""
    sql = "select time from vrecord_watchtime where userid=%s and createtime='%s'" % (uid, yesterday)
    result = dictfetchall(sql)
    time = result[0]['time'] if result else 0
    return second_to_hour(time)


def get_newer_course(uid):
    """获取最新课程"""
    sql = "select * from vrecord_watchrecord where user_id=%s  order by createtime desc limit 1 " % uid
    result = dictfetchall(sql)
    videoid = result[0]['video_id'] if result else None
    if videoid:
        obj = Video.objects.get(id=videoid)
        return '%s > %s' % (obj.course.name, obj.name)
    else:
        return ''



def get_timu_status(uid, yesterday=None):
    """获取昨日答题正确率"""
    if yesterday:
        sql = "select * from  vrecord_watchtimu where userid = %s and createtime='%s'" % (uid, yesterday)
        result = dictfetchall(sql)
        if result:
            flag = 0
            for item in result:
                if item['status'] == '0':
                    flag += 1
            return '%.2f%%' % (flag/1.0/len(result)*100)
        else:
            return '0.00%'
    else:
        sql = "select * from  vrecord_watchtimu where userid = %s" % (uid)
        result = dictfetchall(sql)
        flag = 0
        if result:
            for item in result:
                if item['status'] == '0':
                    flag += 1
            return '%.2f%%' % (flag / 1.0 / len(result) * 100)
        else:
            return '0.00%'


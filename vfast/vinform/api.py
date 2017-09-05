#!/usr/bin/env python
#encoding:utf-8
from vfast.api import dictfetchall, second_to_hour

def get_score_yesterday(uid, yesterday):
    """获取昨日总得分"""
    sql = "select sum(score) as score from vrecord_score where createtime='%s' and user_id=%s;" % (yesterday, uid)
    result = dictfetchall(sql)
    score = result[0]['score'] if result[0]['score'] else 0
    return score


def get_videotime_yesterday(uid,yesterday):
    """获取昨日观看视频总时长"""
    sql = "select time from vrecord_watchtime where uid=%s and createtime='%s'" % (uid, yesterday)
    result = dictfetchall(sql)
    time = result[0]['score'] if result[0]['score'] else 0
    return second_to_hour(time)


def get_newer_course(uid):
    """获取最新课程"""
    pass


def get_timu_yesterday(uid, yesterday):
    """获取昨日答题正确率"""
    pass


def get_timu_average(uid):
    """获取平均答题正确率"""
    pass


def get_track_finished(uid, pathid):
    pass
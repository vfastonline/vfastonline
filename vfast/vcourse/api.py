#!/usr/bin/env python
#encoding: utf-8
import logging
import traceback

from vcourse.models import Video
from vfast.api import dictfetchall
from vrecord.models import WatchRecord


def course_process(uid, cid):
    try:
        c_sql = "select count(1) as count from vcourse_video where course_id=%s;" % cid
        wc_sql = "select count(1) as count from vrecord_watchrecord where user_id=%s and course_id = %s and status=0;" % (uid, cid)
        c = dictfetchall(c_sql)[0]['count']
        wc = dictfetchall(wc_sql)[0]['count']
        return ('%.2f%%' % ((wc / 1.0 / c) * 100), '%s/%s' % (wc, c))
    except:
        logging.getLogger().error(traceback.format_exc())
        return ('0.00%', '0/%s' % c)



def track_process(uid, sequence):
    """
    :param uid: 最终用户id
    :param sequence: 指定路线下所有课程
    :return:
    """
    p_num = 0
    try:
        p_num = Video.objects.filter(course__in=sequence).count()
        v_num = WatchRecord.objects.filter(course__in=sequence, user=uid, status=0).count()

        jindu = v_num / 1.0 / p_num
        return ('%.2f%%' % (jindu * 100), '%s/%s' % (v_num, p_num))
    except:
        traceback.print_exc()
        logging.getLogger().error(traceback.format_exc())
        return ('0.00%', '0/%s' % p_num)

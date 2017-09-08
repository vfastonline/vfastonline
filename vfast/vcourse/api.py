#!/usr/bin/env python
#encoding: utf-8
import logging
import traceback
from vfast.api import dictfetchall

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
    try:
        p_num_sql = 'select count(1) as sum from vcourse_video where course_id in (%s)' % sequence
        v_num_sql = 'select COUNT(1) as sum from vrecord_watchrecord where course_id in  (%s) AND user_id = %s  AND status = 0' % (
            sequence, uid)
        p_num = dictfetchall(p_num_sql)[0]['sum']
        v_num = dictfetchall(v_num_sql)[0]['sum']
        jindu = v_num / 1.0 / p_num
        return ('%.2f%%' % (jindu * 100), '%s/%s' % (v_num, p_num))
    except:
        logging.getLogger().error(traceback.format_exc())
        return ('0.00%', '0/%s' % p_num)

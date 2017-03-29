#!encoding: utf-8
from vfast.api import dictfetchall
from django.http import HttpResponse

import logging
import traceback


def sum_score_tech(uid):
    try:
        sql = 'select vp.name, vp.color, tmp.technology_id, tmp.score  from (select technology_id , sum(score) as score  from vrecord_score where user_id = %s group by technology_id) as tmp left join vcourse_program as vp on vp.id=tmp.technology_id;' % uid
        result = dictfetchall(sql)
        for item in result:
            item['score'] = str(item['score'])
        return result
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')

#!encoding: utf-8
from vfast.api import dictfetchall
from vcourse.models import Technology
import logging
import traceback


def sum_score_tech(uid):
    try:
        sql = 'select vp.name, vp.color, tmp.technology_id, tmp.score  from (select technology_id , sum(score) as score  from vrecord_score where user_id = %s group by technology_id) as tmp left join vcourse_technology as vp on vp.id=tmp.technology_id;' % uid
        result = dictfetchall(sql)
        teches = Technology.objects.all().values()
        technames = [ k['name'] for k in result]
        for tech in teches:
            for item in result:
                item['score'] = str(item['score'])
            if tech['name'] not in technames:
                tmp = dict()
                tmp['color'] = tech['color']
                tmp['name'] = tech['name']
                tmp['technology_id'] = tech['id']
                tmp['score'] = '0'
                result.append(tmp)
        return result
    except:
        logging.getLogger().error(traceback.format_exc())
        return []



def track_skill(user):
    """用户加入一个路线,  返回掌握的技能, 未掌握的技能"""
    try:
        pathid = user.pathid
        sql = "select p_sequence from vcourse_path where id = %s" % pathid
        cids = dictfetchall(sql)[0]['p_sequence']
        # print cids
        sql2 = "select id as section_id, course_id, skill from vcourse_section where course_id in (%s) " % cids
        # print sql2
        sections = dictfetchall(sql2)
        gain_skill, skill = [], []
        for value in sections:
            sql3 = "select id as video_id from vcourse_video where section_id = %s" % value['section_id']
            video_ids = dictfetchall(sql3)
            vids = [str(i['video_id']) for i in video_ids]
            sql4 = "select count(1) as count from vrecord_watchrecord where status=0 and user_id = %s and video_id in (%s)" % (user.id, ','.join(vids))
            learned_video_in_section = dictfetchall(sql4)[0]['count']
            # print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            # print sql4
            # print learned_video_in_section, len(video_ids), type(len(video_ids)), type(learned_video_in_section)
            # print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
            if learned_video_in_section == len(video_ids):
                gain_skill.append(value['skill'])
            else:
                skill.append(value['skill'])
        return gain_skill, skill
    except:
        logging.getLogger().error(traceback.format_exc())
        return [], []





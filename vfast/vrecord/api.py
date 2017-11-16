#!encoding: utf-8
import logging

from vcourse.models import *
from vfast.api import dictfetchall
from vrecord.models import *


def sum_score_tech(uid):
    try:
        sql = 'select vp.name, vp.color, tmp.technology_id, tmp.score  from (select technology_id , sum(score) as score  from vrecord_score where user_id = %s group by technology_id) as tmp left join vcourse_technology as vp on vp.id=tmp.technology_id;' % uid
        result = dictfetchall(sql)
        teches = Technology.objects.all().values()
        technames = [k['name'] for k in result]
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
    """用户加入一个路线,  返回掌握的技能, 未掌握的技能
    :param user: 用户对象
    :return:
    """
    gain_skill, skill = [], []
    try:
        paths = Path.objects.filter(id=user.pathid)
        if paths.exists():
            courses, courses_values = paths[0].get_after_sorted_course()
            sections = Section.objects.filter(course__in=courses)
            for one_section in sections:
                videos = Video.objects.filter(section=one_section)
                learned_video_in_section = WatchRecord.objects.filter(user=user, video__in=videos).count()
                if learned_video_in_section == videos.count():
                    gain_skill.append(one_section.skill)
                else:
                    skill.append(one_section.skill)
    except:
        logging.getLogger().error(traceback.format_exc())
    finally:
        return gain_skill, skill

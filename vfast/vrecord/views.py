#!encoding: utf-8
# from django.shortcuts import render
from vuser.models import User
from vcourse.models import Course, Video, Technology
from vrecord.models import WatchRecord, Score, WatchCourse
from django.http import HttpResponse
from django.db import connection
from vbadge.models import UserBadge, Badge
from vfast.api import get_day_of_day, dictfetchall

import time
import json
import logging, traceback


def user_level(user):
    try:
        score = user.totalscore
        # level = score / 150 + 1
        # if headframobj.url == user.headimgframe:
        #     logging.getLogger().info('用户等级没有改变')
        #     return False, None
        # else:
        #     user.headimgframe = headframobj.url
        #     logging.getLogger().info('用户等级增加为%s' % level)
        #     return True, level
    except:
        logging.getLogger().error(traceback.format_exc())
        return False, None


def course_watched_all(user, course, tech):
    try:
        t = time.strftime('%Y-%m-%d')
        c_videos = Video.objects.filter(course=course).__len__()
        w_videos = WatchRecord.objects.filter(user=user, course=course, status=0).__len__()

        # 用户看完一个课程系类, 获得30积分, 以及对应的勋章
        if c_videos == w_videos:
            Score.objects.create(user=user, technology=tech, createtime=t, score=30)
            user.totalscore = user.totalscore + 30
            logging.getLogger().info('用户%s获得积分30分' % user.username)
            badge = Badge.objects.get(course=course)
            UserBadge.objects.create(createtime=t, badge=badge, user=user)
            WatchCourse.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S'), user=user, course=course)
            logging.getLogger().info('用户%s获得%s勋章' % (user.username, badge.badgename))
            return True, {'badge_name': badge.badgename, 'badge_url': badge.badgeurl}
        else:
            return False, None
    except:
        logging.getLogger().error(traceback.format_exc())
        return False, None


def record_video(request):
    """记录用户观看课程视频的时间点, 以及课程是否观看完成
    """
    try:
        if request.method == 'GET':
            uid = request.session["user"]["id"]  # userid
            vid = request.GET.get('vid')  # videoid
            video_process = request.GET.get('video_process')  # 观看视频时间点
            status = request.GET.get('status')  # 视频是否观看完成
            status = int(status)

            user = User.objects.get(id=uid)
            video = Video.objects.get(id=vid)
            course = Course.objects.get(id=video.course_id)
            try:
                obj = WatchRecord.objects.get(user=user, video=video, course=course)
                if status == 0 and obj.status == 0:
                    obj.video_process = 0
                    obj.createtime = time.strftime('%Y-%m-%d %H:%M:%S')
                    obj.save()
                    return HttpResponse(json.dumps({'code': 0, 'b_flag': False, 'l_flag': False}, ensure_ascii=False))

                elif status == 0 and obj.status == 1:
                    obj.status = status
                    obj.video_time = video_process
                    obj.video_process = 0
                    obj.save()
                    tech = Technology.objects.get(id=course.tech_id)
                    Score.objects.create(user=user, technology=tech, createtime=time.strftime('%Y-%m-%d'), score=1)
                    user.totalscore = user.totalscore + 1
                    b_flag, badge = course_watched_all(user, course, tech)  # 增加分数,查看是否获得勋章
                    l_flag, rlevel = user_level(user)  # 等级是否变更
                    user.save()
                    return HttpResponse(
                        json.dumps({'code': 0, 'b_flag': b_flag, 'badge': badge, 'l_flag': l_flag, 'rlevel': rlevel},
                                   ensure_ascii=False))
                else:
                    obj.createtime = time.strftime('%Y-%m-%d %H:%M:%S')
                    obj.video_process = video_process
                    obj.video_time = video_process
                    obj.save()
                    return HttpResponse(json.dumps({'code': 0, 'b_flag': False, 'l_flag': False}, ensure_ascii=False))

            except WatchRecord.DoesNotExist:
                WatchRecord.objects.create(user=user, video=video, course=course, status=status,
                                           video_process=video_process, video_time=video_process,
                                           createtime=time.strftime('%Y-%m-%d %H:%M:%S'))
                return HttpResponse(json.dumps({'code': 0, 'b_flag': False, 'l_flag': False}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': traceback.format_exc()}, ensure_ascii=False))


def get_score_seven_day(request):
    try:
        uid = request.session['user']['id']
        seven_day = []
        for i in range(-7, 1):
            tmp = {}
            tmp['date'] = str(get_day_of_day(i))
            tmp['label'] = str(get_day_of_day(i))
            # 获取最近七天的得分
            sql = """select sum(score) as score from vrecord_score where createtime = '%s' and user_id = %s""" % (
                str(get_day_of_day(i)), uid)
            ret = dictfetchall(sql)
            if ret[0]['score'] is None:
                tmp['value'] = 0
            else:
                tmp['value'] = int(ret[0]['score'])
            seven_day.append(tmp)
        return HttpResponse(json.dumps({'weekscore': seven_day}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(' error')


def get_score_thirty_day(request):
    try:
        date = request.GET.get('date')
        uid = request.GET.get('uid')
        sql = "select createtime, sum(score) as score from vrecord_score where user_id=%s and createtime like '%s%%' group by createtime order by createtime;" % (
            uid, date)
        ret = dictfetchall(sql)
        result = {}
        for item in ret:
            if item['createtime'][-2:].startswith('0'):
                key = item['createtime'][-2:][-1:]
                result[str(key)] = str(item['score'])
            else:
                key = item['createtime'][-2:]
                result[str(key)] = str(item['score'])
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')

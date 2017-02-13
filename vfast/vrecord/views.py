#!encoding: utf-8
# from django.shortcuts import render
from vuser.models import User
from vcourse.models import Course, Video, Program
from vrecord.models import WatchRecord, Score
from django.http import HttpResponse
from django.db.models import Sum
from django.db import connection
from vbadge.models import UserBadge, Badge
from vgrade.models import Headframe

import time
import json
import logging, traceback


def user_level(user):
    try:
        score = Score.objects.filter(user=user).aggregate(score=Sum('score'))['score']
        level = score / 150 + 1
        headframobj = Headframe.objects.get(id=level)
        print score, level, headframobj.url, user.headimgframe
        if headframobj.url == user.headimgframe:
            logging.getLogger().info('用户等级没有改变')
            return False
        else:
            user.headimgframe = headframobj.url
            user.save()
            logging.getLogger().info('用户等级增加为%s' % level)
            return {'level': level}
    except:
        logging.getLogger().error(traceback.format_exc())


def course_watched_all(user, course, tech, t):
    try:
        c_videos = Video.objects.filter(course=course).__len__()
        w_videos = WatchRecord.objects.filter(user=user, course=course, status=0).__len__()
        # 用户看完一个课程系类, 获得30积分, 以及对应的勋章
        if c_videos == w_videos:
            Score.objects.create(user=user, technology=tech, createtime=t, score=30)
            logging.getLogger().info('用户%s获得积分30分' % user.username)
            badge = Badge.objects.get(course=course)
            UserBadge.objects.create(createtime=t, badge=badge, user=user)
            logging.getLogger().info('用户%s获得%s勋章' % (user.username, badge.badgename))
            print badge.badgename, badge.badgeurl
            return {'badgename': badge.badgename, 'badgeurl': badge.badgeurl}
        else:
            return False
    except:
        logging.getLogger().error(traceback.format_exc())
        return False


# Create your views here.
def record_video(request):
    """记录用户观看课程视频的时间点, 以及课程是否观看完成
    """
    try:
        if request.method == 'POST':
            uid = request.POST.get('uid')  # userid
            vid = request.POST.get('vid')  # videoid
            video_process = request.POST.get('video_process')  # 观看视频时间点
            status = request.POST.get('status')  # 视频是否观看完成
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            user = User.objects.get(id=uid)
            video = Video.objects.get(id=vid)
            course = Course.objects.get(id=video.course_id)
            try:
                obj = WatchRecord.objects.get(user=user, video=video, course=course)
                if obj.status == 0:
                    obj.video_process = video_process
                    obj.save()
                    # logging.getLogger().info(connection.queries)
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'视频已看完'}, ensure_ascii=False))
                else:
                    obj.status = status
                    obj.createtime = t
                    obj.video_time = video_process
                    tech = Program.objects.get(id=course.tech_id).id
                    if int(status) == 0:
                        obj.video_process = 0
                        obj.save()
                        tech = Program.objects.get(id=course.tech_id)
                        Score.objects.create(user=user, technology=tech, createtime=t, score=1)
                        r_badge = course_watched_all(user, course, tech, t)  # 增加分数,查看是否获得勋章
                        r_level = user_level(user)  # 等级是否变更
                        # logging.getLogger().info(connection.queries)
                        return HttpResponse(
                            json.dumps({'code': 0, 'result': {'badge': r_badge, 'level': r_level}}, ensure_ascii=False))
                    else:
                        obj.video_process = video_process
                        obj.save()
                        logging.getLogger().info(connection.queries)
                        return HttpResponse(json.dumps({'code': 0, 'result': {}}))
            except WatchRecord.DoesNotExist:
                WatchRecord.objects.create(user=user, video=video, course=course, status=status,
                                           video_process=video_process, video_time=video_process, createtime=t)
                if int(status) == 0:
                    tech = Program.objects.get(id=course.tech_id)
                    course = Course.objects.get(id=video.course_id)
                    Score.objects.create(user=user, technology=tech, createtime=t, score=1)
                    r_badge = course_watched_all(user, course, tech, t)
                    r_level = user_level(user=user)
                    # logging.getLogger().info(connection.queries)
                    return HttpResponse(
                        json.dumps({'code': 0, 'result': {'badge': r_badge, 'level': r_level}}, ensure_ascii=False))
                else:
                    # logging.getLogger().info(connection.queries)
                    return HttpResponse(json.dumps({'code': 0, 'result': {}}))
        else:
            return HttpResponse('get method~!')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))

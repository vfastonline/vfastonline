#!encoding: utf-8
# from django.shortcuts import render
from vuser.models import User
from vcourse.models import Course, Video, Program
from vrecord.models import WatchRecord, Score
from django.http import HttpResponse
from django.db.models import F
from vbadge.models import UserBadge, Badge

import time
import json
import logging, traceback


def course_watched_all(user, course, tech, t):
    """判断用户是否看完一个课程的全部视频"""
    c_videos = Video.objects.filter(course=course).__len__()
    w_videos = WatchRecord.objects.filter(user=user, course=course, status=0).__len__()
    if c_videos == w_videos:
        Score.objects.create(user=user, technology=tech, createtime=t, score=30)
        logging.getLogger().info('用户%s获得积分30分' % user.username)
        badge = Badge.objects.get(course=course)
        UserBadge.objects.create(createtime=t, badge=badge, user=user)
        logging.getLogger().info('用户%s获得%s勋章' % (user.username, badge.badgename))


# Create your views here.
def record_video(request):
    """记录用户观看课程视频的时间点, 以及课程是否观看完成
    uid=1&vid=2&video_process=1500&status=0
    后台需要查找cid, techid,
    """
    try:
        if request.method == 'POST':
            uid = request.POST.get('uid')
            vid = request.POST.get('vid')
            video_process = request.POST.get('video_process')
            status = request.POST.get('status')
            # print type(status), status
            t = time.strftime('%Y-%m-%d %H:%M:%S')

            user = User.objects.get(id=uid)
            video = Video.objects.get(id=vid)
            course = Course.objects.get(id=video.course_id)
            tech = Program.objects.get(id=course.tech_id)

            try:
                obj = WatchRecord.objects.get(user=user, video=video, course=course)
                if obj.status == 0:
                    obj.video_process = video_process
                    obj.save()
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'视频已看完'}, ensure_ascii=False))
                else:
                    obj.status = status
                    obj.video_process = 0
                    obj.createtime = t
                    if int(status) == 0:
                        print 'video_time'
                        obj.video_time = video_process
                        obj.save()
                        Score.objects.create(user=user, technology=tech, createtime=t, score=1)
                        #如果用户看完了一个课程所有的视频,给用户发勋章
                        course_watched_all(user, course, tech, t)
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'video update'}))
            except WatchRecord.DoesNotExist:
                WatchRecord.objects.create(user=user, video=video, course=course, status=status,
                                           video_process=video_process, video_time=video_process,
                                           createtime=t)
                if int(status) == 0:
                    print 'not exits add'
                    Score.objects.create(user=user,technology=tech, createtime=t, score=1)
                    course_watched_all(user, course)
                return HttpResponse('create record ok')
        else:
            return HttpResponse('get method~!')

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))






#!encoding: utf-8
# from django.shortcuts import render
from vuser.models import User
from vcourse.models import Course, Video
from record.models import WatchRecord, Score
import time
import json
from django.http import HttpResponse
import logging, traceback


# Create your views here.
def record_video(request):
    """记录用户观看课程视频的时间点
    uid=1&vid=2&cid=1&video_progress=14433111&status=0
    """
    try:
        if request.method == 'POST':
            uid = request.POST.get('uid')
            vid = request.POST.get('vid')
            cid = request.POST.get('cid')
            video_progress = request.POST.get('video_progress', 0)
            status = request.POST.get('status')
            t = time.strftime('%Y-%m-%d %H:%M:%S')

            user = User.objects.get(id=uid)
            video = Video.objects.get(id=vid)
            course = Course.objects.get(id=cid)

            try:
                obj = WatchRecord.objects.get(user=user, video=video, course=course)
                if obj.status == 0:
                    return HttpResponse(json.dumps({'code':0, 'msg':u'视频已看完'}, ensure_ascii=False))
                else:
                    obj.status = status
                    obj.video_progress = video_progress
                    obj.recordtime = t
                    obj.save()
                    # WatchRecord.objects.filter(user=user, video=video, course=course).update(status=status, video_progress=video_progress,
                    #                                                                          recordtime=t)
                    return HttpResponse(json.dumps({'code':0, 'msg':u'video update'}))
            except WatchRecord.DoesNotExist:
                WatchRecord.objects.create(user=user, video=video,
                                           course=course,
                                           status=status,
                                           video_progress=video_progress,
                                           recordtime=t)
                return HttpResponse('create record ok')
        else:
            return HttpResponse('get method~!')

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def record_score(request):
    """记录用户针对每个课程获取的积分"""
    try:
        if request.method == "POST":
            uid = request.POST.get('uid')
            cid = request.POST.get('cid', None)
            score = request.POST.get('score')
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')

            user = User.objects.get(id=uid)
            course = Course.objects.get(id=cid) if cid else None

            result = Score.objects.create(user=user, course=course, score=score,
                                          createtime=createtime) if course else Score.objects.create(userid=user,
                                                                                                     score=score,
                                                                                                     createtime=createtime)
            return HttpResponse('ok')
        else:
            return HttpResponse('get method')

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))

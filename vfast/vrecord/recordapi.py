#!encoding:utf-8
from record.models import Score, WatchRecord
from vuser.models import User
from vcourse.models import Video, Course
from django.db.models import Sum


def get_score(model, uid=None):
    """获取用户积分, 排行榜"""
    if uid:
        user = User.objects.get(id=uid)
        result = model.objects.values('user_id').annotate(sumscore=Sum('score')).all().filter(userid=user)
    else:
        result = model.objects.values('user_id').annotate(sum=Sum('score')).all().order_by('-sum')[0:3]
    return result


def get_watchtime(model, uid=None):
    """获取用户积分, 排行榜"""
    if uid:
        user = User.objects.get(id=uid)
        result = model.objects.values('user_id').annotate(sumscore=Sum('video_progress')).all().filter(userid=user)
    else:
        result = model.objects.values('user_id').annotate(sum=Sum('video_progress')).all().order_by('-sum')[0:3]
    return result


def get_watched_video(uid, cid):
    """获取用户观看视频信息列表"""
    course = Course.objects.get(id=cid)
    videos = Video.objects.filter(course=course).all().values()
    user = User.objects.get(id=uid)
    user_watched = WatchRecord.objects.filter(user=user).all().values()

    for video in videos:
        for watch in user_watched:
            if video['id'] == watch['id']:
                # print "用户观看过这个视频", watch['status']
                video.update({'status': watch['status'], 'video_progress': watch['video_progress']})
            else:
                # print '用户没有观看过这个视频'
                video.update({'status': 'no', 'video_progress': 0})
    return videos

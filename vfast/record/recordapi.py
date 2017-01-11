#!encoding:utf-8
from record.models import Score, WatchRecord
from vuser.models import User
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


#!encoding: utf-8
# from django.shortcuts import render
from vuser.models import User
from vcourse.models import Course, Video, Technology, Path
from vrecord.models import WatchRecord, Score, WatchCourse, Watchtime, WatchTimu, Watchface
from vpractice.models import Timu
from django.http import HttpResponse
from django.db import connection
from vbadge.models import UserBadge, Badge
from vfast.api import get_day_of_day, dictfetchall, require_login

import time
import json
import logging, traceback


def test(request):
    user = User.objects.get(id=19)
    get_track_badge(user=user, cid=3)
    return HttpResponse('ok')


def get_mengxin(user):
    """给用户发送萌新勋章"""
    try:
        score = user.totalscore
        logging.getLogger().info('开始判断是否给用户%s萌新勋章' % user.nickname)
        if score > 10:
            mengxin_badge = Badge.objects.get(badgename='mengxin')
            if UserBadge.objects.filter(user=user, badge=mengxin_badge).__len__() == 0:
                UserBadge.objects.create(user=user, badge=mengxin_badge, createtime=time.strftime('%Y-%d-%m'))
                user.totalscore += 30
                logging.getLogger().info('用户%s获得萌新勋章' % user.nickname)
                return [
                    dict(name=mengxin_badge.badgename, url=mengxin_badge.large_url.url, desc=mengxin_badge.description)]
            else:
                logging.getLogger().info('用户%s之前获得萌新勋章' % user.nickname)
                return []
        else:
            logging.getLogger().info('用户%s不能获得萌新勋章' % user.nickname)
            return []
    except:
        logging.getLogger().error(traceback.format_exc())
        return []


def get_track_badge(user, cid, cname):
    try:
        logging.getLogger().info('用户%s学完课程%s, 判断是否给用户%s发送相关路线勋章' % (user.nickname, cname, user.nickname))
        paths = Path.objects.all().values('id', 'p_sequence')
        watched_courses = WatchCourse.objects.filter(user=user)
        user_wathced_cids, tracks = [], []
        for item in watched_courses:
            user_wathced_cids.append(str((item.course.id)))

        for path in paths:
            path_cids = path['p_sequence'].split(',')
            print path_cids
            if (str(cid) in path_cids) and (not set(path_cids).difference(user_wathced_cids)):
                path = Path.objects.get(id=int(path['id']))
                # print path.name
                badge = Badge.objects.get(path=path)
                if UserBadge.objects.filter(user=user, badge=badge).__len__() == 0:
                    UserBadge.objects.create(user=user, badge=badge, createtime=time.strftime('%Y-%d-%m'))
                    user.totalscore += 30
                    logging.getLogger().info('用户%s成功获取%s路线勋章' % (user.nickname, badge.path.name))
                    tracks.append(dict(name=badge.badgename, url=badge.large_url.url, desc=badge.description))
                else:
                    logging.getLogger().info('用户%s之前获取%s路线勋章' % (user.nickname, badge.path.name))
        return tracks
    except:
        logging.getLogger().error(traceback.format_exc())
        return []


def course_watched_all(user, course, tech):
    try:
        t = time.strftime('%Y-%m-%d')
        c_videos = Video.objects.filter(course=course).__len__()
        w_videos = WatchRecord.objects.filter(user=user, course=course, status=0).__len__()

        # 用户看完一个课程系类, 获得30积分, 以及对应的勋章
        if c_videos == w_videos:
            Score.objects.create(user=user, technology=tech, createtime=t, score=30)
            user.totalscore = user.totalscore + 30
            logging.getLogger().info('用户%s获得积分30分' % user.nickname)
            badge = Badge.objects.get(course=course)
            if not UserBadge.objects.filter(badge=badge, user=user):
                UserBadge.objects.create(createtime=t, badge=badge, user=user)
                WatchCourse.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S'), user=user, course=course)
                logging.getLogger().info('用户%s获得%s勋章' % (user.nickname, badge.badgename))
                return [{'name': badge.badgename, 'url': badge.large_url.url}]
        else:
            return []
    except:
        logging.getLogger().error(traceback.format_exc())
        return []


@require_login()
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
            today = time.strftime('%Y-%m-%d %H:%M:%S')
            t = time.strftime('%Y-%m-%d')

            try:
                watchtime_obj = Watchtime.objects.get(userid=user.id, createtime=t)
                watchtime_obj.time += 10
                watchtime_obj.save()
            except:
                Watchtime.objects.create(userid=user.id, time=10, createtime=t)

            try:
                obj = WatchRecord.objects.get(user=user, video=video, course=course)
                if status == 0 and obj.status == 0:
                    obj.video_process = 0
                    obj.createtime = today
                    obj.save()
                    return HttpResponse(
                        json.dumps({'code': 1, 'course': [], 'mengxin': [], 'tracks': []}, ensure_ascii=False))

                elif status == 0 and obj.status == 1:
                    obj.status = status
                    obj.video_time = video_process
                    obj.video_process = 0
                    obj.save()
                    tech = Technology.objects.get(id=course.tech_id)
                    Score.objects.create(user=user, technology=tech, createtime=today, score=1)
                    user.totalscore = user.totalscore + 1

                    course_badge = course_watched_all(user, course, tech)  # 增加分数,查看是否获得勋章
                    mengxin = get_mengxin(user)
                    if course_badge:
                        tracks = get_track_badge(user, cid=course.id, cname=course.name)
                    else:
                        tracks = []
                    user.save()
                    return HttpResponse(
                        json.dumps({'code': 0, 'course': course_badge, 'mengxin': mengxin, 'tracks': tracks},
                                   ensure_ascii=False))
                elif status == 1 and obj.status == 0:
                    obj.video_process = video_process
                    obj.createtime = today
                    obj.save()
                    return HttpResponse(
                        json.dumps({'code': 2, 'course': [], 'mengxin': [], 'tracks': []}, ensure_ascii=False))
                else:
                    obj.createtime = today
                    obj.video_process = video_process
                    obj.video_time = video_process
                    obj.save()
                    return HttpResponse(
                        json.dumps({'code': 3, 'course': [], 'mengxin': [], 'tracks': []}, ensure_ascii=False))

            except WatchRecord.DoesNotExist:
                WatchRecord.objects.create(user=user, video=video, course=course, status=status,
                                           video_process=video_process, video_time=video_process,
                                           createtime=today)
                return HttpResponse(
                    json.dumps({'code': 4, 'course': [], 'mengxin': [], 'tracks': []}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def get_score_seven_day(request):
    try:
        uid = request.GET.get('uid', None)
        if not uid:
            return HttpResponse(json.dumps({'code': 1, 'msg': 'parameter error!'}))
        date, score, vtime = [], [], []
        for i in range(-7, 1):
            date.append(str(get_day_of_day(i)))
            # 获取最近七天的得分
            sql_score = """select sum(score) as score from vrecord_score where createtime = '%s' and user_id = %s""" % (
                str(get_day_of_day(i)), uid)
            ret = dictfetchall(sql_score)
            if ret[0]['score'] is None:
                score.append(0)
            else:
                score.append(int(ret[0]['score']))
            # 获取最近七天的观看时长
            sql_vtime = """select * from vrecord_watchtime where userid=%s and createtime='%s'; """ % (
                uid, str(get_day_of_day(i)))
            ret_time = dictfetchall(sql_vtime)
            if ret_time:
                vtime.append(ret_time[0]['time'])
            else:
                vtime.append(0)
        result = {'date': date, 'score': score, 'vtime': vtime}
        return HttpResponse(json.dumps({'result': result}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


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
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


@require_login()
def record_timu(request):
    try:
        today = time.strftime('%Y-%m-%d')
        userid = request.session['user']['id']
        timuid = request.GET.get('timuid')
        timu = Timu.objects.get(id=timuid)
        skill = timu.video.section.skill
        courseid = request.GET.get('courseid')
        status = request.GET.get('status')
        try:
            obj = WatchTimu.objects.get(userid=userid, timuid=timuid)
            obj.status = status
            obj.createtime = today
            obj.save()
        except WatchTimu.DoesNotExist:
            WatchTimu.objects.create(userid=userid, createtime=today, status=status, timuid=timuid, courseid=courseid, skill=skill)
        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))



# @require_login()
def face(request):
    """记录用户观看视频时表情状态"""
    try:
        if request.method == "POST":
            userid = 1
            joy = request.POST.get('joy')
            joy = round(float(request.POST.get('joy')[0]),3)
            engagement = round(float(request.POST.get('engagement')[0]),3)
            sadness = round(float(request.POST.get('sadness')[0]),3)
            anger = round(float(request.POST.get('anger')[0]),3)
            surprise = round(float(request.POST.get('surprise')[0]),3)
            fear = round(float(request.POST.get('fear')[0]),3)
            valence = round(float(request.POST.get('valence')[0]),3)
            contempt = round(float(request.POST.get('contempt')[0]),3)
            vtime = request.POST.get('vtime',0)
            vtime = int(vtime.split('.')[0])
            logging.getLogger().info('%s %s  %s  %s %s' % (engagement, surprise, valence, contempt,vtime))
            Watchface.objects.create(userid=userid,joy=joy,engagement=engagement, sadness=sadness,anger=anger,
                                     surprise=surprise, fear=fear,valence=valence,contempt=contempt,vtime=vtime)
        return HttpResponse(json.dumps({'code':0}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


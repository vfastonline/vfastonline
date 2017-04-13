#!encoding:utf-8
import logging, traceback
import json
import os
import time

from vfast.api import require_role, require_login, dictfetchall
from vuser.models import User
from vcourse.models import Technology, Course, Video, Path, UserPath
from vrecord.models import WatchRecord
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def test(request):
    w = WatchRecord.objects.filter(id=1).values('user__username')
    print w.query
    print w
    from vpractice.models import Replay
    r = Replay.objects.filter(id=1).values('question__user__username')
    print r.query
    print r
    return render(request, "search_Result.html")


def getpath(request):
    """获取学习路线详细信息, 学习路线下包含的所有课程
        path为path对象, courseall包含所有的course对象
    """
    try:
        pid = request.GET.get('id')
        path = Path.objects.get(id=pid)
        sequence = path.p_sequence
        course = sequence.split(',')
        try:
            uid = request.session['user']['id']
            path_id = User.objects.get(id=uid).pathid
        except:
            path_id = ''
        courses = []
        for cid in course:
            c = Course.objects.get(id=cid)
            videos = Video.objects.filter(course=c).values()
            courses.append(dict(course=c, video=videos))

        return render(request, 'learnPath_show.html',
                      {'path': path, 'path_id': path_id, 'courses': courses, 'xingxing': [0, 1, 2, 3, 4]})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getcourses(request):
    """获取所有的课程"""
    try:
        pubs, not_pubs = [], []
        type = request.GET.get('type', None)
        vps = Technology.objects.all().values()
        try:
            techobj = Technology.objects.get(name=type)
            courses = Course.objects.filter(tech=techobj).values('id')
        except:
            courses = Course.objects.filter().values('id')
            techobj = ''
        print courses
        for c in courses:
            sql_pub = "select vc.*, vv.vtype, vv.id as video_id, vv.sequence, vt.name as vt_name, vt.color as vt_color from vcourse_technology as vt, vcourse_course as vc, vcourse_video as vv where vt.id=vc.tech_id and vv.course_id=vc.id and vc.id=%s order by sequence limit 1" % \
                      c['id']
            print sql_pub
            ret = dictfetchall(sql_pub)
            if len(ret) != 0:
                pubs.append(ret[0])
            else:
                not_pubs.append(Course.objects.get(id=c['id']))
        print pubs, not_pubs
        return render(request, 'course_library.html',
                      {'pubs': pubs, 'not_pubs': not_pubs, 'vps': vps, 'tech_obj': techobj,
                       'xingxing': [0, 1, 2, 3, 4]})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getpaths(request):
    """获取所有的路线"""
    try:
        paths = Path.objects.all()
        print paths
        return render(request, 'learning_path.html', {'paths': paths})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


@require_login()
def join_path(request):
    try:
        pid = request.GET.get('pid')
        uid = request.session['user']['id']
        user = User.objects.get(id=uid)
        path = Path.objects.get(id=pid)
        sequence = path.p_sequence
        User.objects.filter(id=uid).update(pathid=pid)
        if UserPath.objects.filter(user=user, path=path).exists():
            video = WatchRecord.objects.filter(user=user, course_id__in=sequence).order_by('-createtime').values(
                'video_id', 'video__vtype', 'createtime').first()
            url = '/video/%s' % video['video_id'] if video['video__vtype'] == 0 else '/practice/%s' % video['video_id']
            return HttpResponseRedirect(url)
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            UserPath.objects.create(user=user, path=path, createtime=t)
            course_id = int(sequence.split(',')[0])
            video = Video.objects.filter(course_id=course_id, sequence=1).values('vtype', 'id').first()
            print video
            url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
            return HttpResponseRedirect(url)
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))

#!encoding:utf-8
from vcourse.models import Course
from django.shortcuts import render
from django.db import connection
from vgrade.api import headimg_urls
import random
from vcourse.models import Program
from vfast.api import get_id_name, require_role, require_login
from vrecord.views import course_watched_all
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from vuser.models import User
from django.db.models import F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from vcourse.models import Video
from vfast.api import dictfetchall

import logging
import traceback
import json


# @require_login()
# @require_role(role=1)
def test(request):
    print 'test'
    # course = connection.cursor()
    # course.execute('select * from vcourse_video')
    # a = dictfetchall(cursor=course)
    return render(request, "search_Result.html")


def dashBoard(request):
    return render(request, 'dashBoard.html')


def learning_path(request):
    return render(request, 'learning_path.html')


def course_library(request):
    return render(request, 'course_library.html')


def learnPath_show(request):
    return render(request, 'learnPath_show.html')


def logout(request):
    # print 'del session'
    # del request.session['token']
    del request.session['login']
    del request.session['user']
    return HttpResponse('del session ok')


# @require_login()
def index(request):
    return render(request, 'index.html')


def search(request):
    try:
        key_words = request.GET.get('query')
        vps = Program.objects.all()
        print key_words
        courses = Course.objects.filter(name__contains=key_words).values('id')
        print courses
        result = []
        for c in courses:
            sql = "select vc.*, vv.vtype, vv.id as video_id, vv.sequence, vp.name as vp_name, vp.color as vp_color from vcourse_program as vp, vcourse_course as vc, vcourse_video as vv where vp.id=vc.tech_id and vv.course_id=vc.id and vc.id=%s order by sequence limit 1" % \
                  c['id']
            ret = dictfetchall(sql)[0]
            result.append(ret)
        print result
        return render(request, 'search_Result.html', {'results':result, 'vps':vps, 'xingxing': [0,1,2,3,4] })
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def search_js(request):
    try:
        course_names = Course.objects.all().values('name')
        cnames = [item['name'] for item in course_names]
        return HttpResponse(json.dumps({'name': cnames}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def playVideo(request, params):
    try:
        print params, type(params)
        video_obj = Video.objects.get(id=int(params))
        try:
            userid = request.session['user']['id']
        except:
            return render(request, 'playVideo.html')
        sql = """select vv.id, vv.name, vv.notes, vv.vurl, vv.vtype, vw.user_id, vv.vtype_url, vv.vtime, vv.course_id,  vw.status from  vcourse_video  as vv left join vrecord_watchrecord as vw  on  vv.id=vw.video_id and vw.user_id=%s where vv.course_id=%s""" % (
        userid, video_obj.course.id)
        videos = dictfetchall(sql)
        print sql
        print videos
        return render(request, 'playVideo.html', {'videos': videos, 'video_obj': video_obj})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(status=404)

def practice(request, params):
    print params
    return render(request, 'playVideo.html')

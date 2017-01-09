#!encoding:utf-8
import logging, traceback
import json
import os
import time

from django.conf import settings
from vuser.models import User
from vcourse.models import TypeFunc, TypeProgram, Course, Video, Path
from vfast.api import get_object
from django.shortcuts import render
from django.http import HttpResponse
from vfast.api import get_object


# Create your views here.
def test(request):
    return HttpResponse('hello,world~!')


def course_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'coursetest.html')
        else:
            name = request.POST.get('name')
            desc = request.POST.get('desc', ' ')
            totaltime = request.POST.get('totaltime', ' ')
            difficult = request.POST.get('difficult', ' ')
            color = request.POST.get('color', ' ')
            pubstatus = request.POST.get('pubstatus', ' ')
            subscibe = request.POST.get('subscibe', ' ')
            order = request.POST.get('order')
            type_func = request.POST.get('type_func')
            type_lang = request.POST.get('type_lang')
            typefunc = TypeFunc.objects.get(id=type_func).id
            typelang = TypeProgram.objects.get(id=type_lang).id
            t = int(time.time())

            print name, desc, totaltime, difficult, color, pubstatus, subscibe, order, type_func, type_lang
            print typefunc, typelang

            result = Course.objects.create(name=name, desc=desc, totaltime=totaltime, difficult=difficult, color=color,
                                           pubstatus=pubstatus, order=order, createtime=t,
                                           subscibe=subscibe, type_func_id=typefunc, type_lang_id=typelang)
            if result:
                return HttpResponse('ok')

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def video_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'coursetest.html')
        else:
            print request.POST
            print request.FILES
            name = request.POST.get('name')
            order = request.POST.get('order')
            videotime = request.POST.get('videotime')
            courseid = request.POST.get('courseid')
            teacherid = request.POST.get('teacherid', 1)
            course = Course.objects.get(id=courseid)
            teacher = User.objects.get(id=teacherid)
            createtime = int(time.time())
            print teacher.username, course.name

            videofile = request.FILES.get('video', None)
            zimufile = request.FILES.get('zimu', None)
            teacher_note_file = request.FILES.get('teacher_note', None)

            day = time.strftime('%Y%m')
            vpath = os.path.join(settings.MEDIA_ROOT, 'video/%s/' % day)
            os.system('mkdir -p  %s' % vpath)

            # 获取需要保存的相对路径
            video = os.path.join('video/%s/%s' % (day, videofile.name)) if videofile else ' '
            zimu = os.path.join('video/%s/%s' % (day, zimufile.name)) if zimufile else ' '
            teacher_note = os.path.join('video/%s/%s' % (day, teacher_note_file.name)) if teacher_note_file else ' '
            print video, zimu, teacher_note, int(videotime)

            for file in [videofile, zimufile, teacher_note_file]:
                try:
                    filename = open(os.path.join(vpath, file.name), 'wb+')
                    for chunk in file.chunks():
                        filename.write(chunk)
                    filename.close()
                except AttributeError:
                    pass
            Video.objects.create(name=name, video=video, zimu=zimu, order=order, videotime=videotime,
                                 teacher_note=teacher_note,
                                 courseid=course, teacher=teacher, createtime=createtime)
            return HttpResponse(json.dumps({'code': 0, u'msg': '上传视频成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def path_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'coursetest.html')
        else:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            jobscount = request.POST.get('jobscount')
            salary = request.POST.get('salary', ' ')
            jobtime = request.POST.get('jobtime', ' ')
            difficult = request.POST.get('difficult', 4)
            totaltime = request.POST.get('totaltime', ' ')
            createtime = int(time.time())
            course = request.POST.getlist('course', [])

            day = time.strftime('%Y%m')
            video = request.FILES.get('video', None)
            img = request.FILES.get('pathimg', None)
            vpath = os.path.join(settings.MEDIA_ROOT, 'video/%s/' % day)
            os.system('mkdir -p  %s' % vpath)

            introvideourl = os.path.join('video/%s/%s' % (day, video.name)) if video else ' '
            pathimg = os.path.join('img/%s/%s' % (day, img.name)) if img else ' '
            print introvideourl, pathimg


            for file in [video, img]:
                try:
                    filename = open(os.path.join(vpath, file.name), 'wb+')
                    for chunk in file.chunks():
                        filename.write(chunk)
                    filename.close()
                except AttributeError:
                    pass

            sql = Path(name=name, desc=desc, introvideourl=introvideourl, jobscount=jobscount, salary=salary,
                       jobtime=jobtime,
                       difficult=difficult, pathimg=pathimg, totaltime=totaltime, createtime=createtime)
            sql.save()
            for courseid in course:
                course = Course.objects.get(id=courseid)
                sql.course.add(course)

            return HttpResponse(json.dumps({'code': 0, 'msg': u'创建路线成功'}, ensure_ascii=False))

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))

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
from vfast.api import get_object, get_results, get_all_results


# Create your views here.
def test(request):
    return HttpResponse('hello,world~!')


def course_add(request):
    """添加课程系列"""
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
    """添加视频"""
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
    """添加学习路线"""
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


def getvideo(request):
    """获取单个视频视频信息"""
    try:
        id = request.GET.get('id')
        video = Video.objects.get(id=id)
        return render(request, 'videodu.html', {'video': video})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getcourse(request):
    """获取课程详细信息, 以及该课程下面所有的视频"""
    try:
        id = request.GET.get('id')
        course = Course.objects.get(id=id)
        videos = Video.objects.filter(courseid=course).all()
        print videos
        print course.name
        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getpath(request):
    """获取学习路线详细信息, 学习路线下包含的所有课程"""
    try:
        id = request.GET.get('id')
        path = Path.objects.get(id=id)
        results = path.course.filter().values().all()  # 获取路线下面的所有课程
        print path.name, results
        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getcourseall(request):
    """获取所有课程, 可以按照语言, 功能分类进行检索"""
    try:
        type_lang = request.GET.get('lang', None)
        type_func = request.GET.get('func', None)
        type_lang_object = TypeProgram.objects.get(id=type_lang) if type_lang else None
        type_func_object = TypeFunc.objects.get(id=type_func) if type_func else None
        if type_func_object and type_lang_object:
            courses = get_all_results(Course, type_lang=type_lang_object, type_func=type_func_object)
        elif type_func_object:
            courses = get_all_results(Course, type_func = type_func_object)
        elif type_lang_object:
            courses = get_all_results(Course, type_lang=type_lang_object)
        else:
            courses = get_all_results(Course)
        print courses
        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))

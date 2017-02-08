#!encoding:utf-8
import logging, traceback
import json
import os
import time

from django.conf import settings
from vuser.models import User
from vcourse.models import Program, Course, Video, Path
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def test(request):
    return HttpResponse('hello,world~!')


def course_add(request):
    """添加课程系列"""
    try:
        if request.method == 'GET':
            return render(request, 'du/coursetest.html')
        else:
            name = request.POST.get('name')
            desc = request.POST.get('desc', ' ')
            totaltime = request.POST.get('totaltime')
            difficult = request.POST.get('difficult', ' ')
            color = request.POST.get('color', ' ')
            pubstatus = request.POST.get('pubstatus')
            pubstatus = int(pubstatus)
            print pubstatus, type(pubstatus)
            icon = request.POST.get('icon')
            tech = request.POST.get('tech')
            teach = request.POST.get('teach')
            techobj = Program.objects.get(id=tech)
            teachobj = User.objects.get(id=teach)
            t = time.strftime('%Y-%m-%d %H:%M:%S')

            print name, desc, totaltime, difficult, color, pubstatus, icon, techobj, teachobj
            result = Course.objects.create(name=name, desc=desc, totaltime=totaltime, difficult=difficult, icon=icon,
                                           color=color, pubstatus=pubstatus, createtime=t, tech=techobj, teach=teachobj)
            if result:
                return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def video_add(request):
    """添加视频"""
    try:
        if request.method == 'GET':
            return render(request, 'du/coursetest.html')
        else:
            print request.POST
            print request.FILES
            name = request.POST.get('name')
            vtime = request.POST.get('vtime')
            courseid = request.POST.get('course')
            order = request.POST.get('order')
            teacherid = request.POST.get('teacher', 1)
            course = Course.objects.get(id=courseid)
            teacher = User.objects.get(id=teacherid)
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            print teacher.username, course.name

            videofile = request.FILES.get('video', None)
            ccfile = request.FILES.get('cc', None)
            notes_file = request.FILES.get('notes', None)

            day = time.strftime('%Y%m%d')
            vpath = os.path.join(settings.MEDIA_ROOT, 'video/%s/' % day)
            os.system('mkdir -p  %s' % vpath)

            # 获取需要保存的相对路径
            vurl = os.path.join(settings.MEDIA_URL, 'video/%s/%s' % (day, videofile.name)) if videofile else ' '
            cc = os.path.join(settings.MEDIA_URL, 'video/%s/%s' % (day, ccfile.name)) if ccfile else ' '
            notes = os.path.join(settings.MEDIA_URL, 'video/%s/%s' % (day, notes_file.name)) if notes_file else ' '
            print vurl, cc, notes, int(vtime)

            for file in [videofile, ccfile, notes_file]:
                try:
                    filename = open(os.path.join(vpath, file.name), 'wb+')
                    for chunk in file.chunks():
                        filename.write(chunk)
                    filename.close()
                except AttributeError:
                    logging.getLogger().error('上传视频是保存文件出错')
            Video.objects.create(name=name, vurl=vurl, cc=cc, vtime=vtime, notes=notes, order=order,
                                 course=course, teacher=teacher, createtime=createtime)
            return HttpResponse(json.dumps({'code': 0, u'msg': '上传视频成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def path_add(request):
    """添加学习路线"""
    try:
        if request.method == 'GET':
            return render(request, 'du/coursetest.html')
        else:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            jobscount = request.POST.get('jobscount')
            salary = request.POST.get('salary', ' ')
            jstime = request.POST.get('jstime', ' ')   #job salary调查时间
            difficult = request.POST.get('difficult', 4)
            totaltime = request.POST.get('totaltime', ' ')
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            orders = request.POST.get('orders')

            day = time.strftime('%Y%m%d')
            intrvfile = request.FILES.get('video', None)
            imgfile = request.FILES.get('pathimg', None)
            vpath = os.path.join(settings.MEDIA_ROOT, 'video/%s/' % day)
            os.system('mkdir -p  %s' % vpath)

            intrv = os.path.join('video/%s/%s' % (day, intrvfile.name)) if intrvfile else ' '
            pathimg = os.path.join('img/%s/%s' % (day, imgfile.name)) if imgfile else ' '
            print intrv, pathimg

            for file in [intrvfile, imgfile]:
                try:
                    filename = open(os.path.join(vpath, file.name), 'wb+')
                    for chunk in file.chunks():
                        filename.write(chunk)
                    filename.close()
                except AttributeError:
                    pass

            sql = Path(name=name, desc=desc, intrv=intrv, jobscount=jobscount, salary=salary, jstime=jstime,
                       orders=orders,
                       difficult=difficult, pathimg=pathimg, totaltime=totaltime, createtime=createtime)
            sql.save()
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




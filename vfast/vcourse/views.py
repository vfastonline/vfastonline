#!encoding:utf-8
import logging, traceback
import json
import os
import time

from vfast.api import require_role, require_login, dictfetchall
from django.conf import settings
from vuser.models import User
from vperm.models import Role
from vcourse.models import Program, Course, Video, Path, UserPath
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

"""现已完成的功能  课程添加, 视频添加, 路线添加, 获取单个视频详情, 单个课程以及所有视频, 所有课程, 路线详情"""


# Create your views here.
def test(request):
    return render(request, "search_Result.html")


@require_login()
def course_add(request):
    """添加课程系列"""
    try:
        if request.method == 'GET':
            techs = Program.objects.filter().values('id', 'name')
            roleobj = Role.objects.get(rolename='teacher')
            teachers = User.objects.filter(role=roleobj).values('id', 'username')
            print techs, teachers
            return render(request, 'du/coursetest.html', {'techs': techs, 'teachers': teachers})
        else:
            name = request.POST.get('name')
            desc = request.POST.get('desc', ' ')
            totaltime = request.POST.get('totaltime')
            difficult = request.POST.get('difficult', ' ')
            color = request.POST.get('color', ' ')
            pubstatus = request.POST.get('pubstatus')
            icon = request.POST.get('icon')
            tech = request.POST.get('tech')
            teach = request.POST.get('teach')
            techobj = Program.objects.get(id=tech)
            teachobj = User.objects.get(id=teach)
            t = time.strftime('%Y-%m-%d %H:%M:%S')

            print pubstatus, icon, teach, tech
            result = Course.objects.create(name=name, desc=desc, totaltime=totaltime, difficult=difficult, icon=icon,
                                           color=color, pubstatus=pubstatus, createtime=t, tech=techobj, teach=teachobj)
            if result:
                return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


@require_role(role=1)
def video_add(request):
    """添加视频"""
    try:
        if request.method == 'GET':
            courses = Course.objects.filter().values('id', 'name')
            return render(request, 'du/coursetest.html', {'courses': courses})
        else:
            print request.POST
            print request.FILES
            name = request.POST.get('name')
            vtime = request.POST.get('vtime')
            courseid = request.POST.get('course')
            course = Course.objects.get(id=courseid)
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            print course.name

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
            try:
                Video.objects.create(name=name, vurl=vurl, cc=cc, vtime=vtime, notes=notes,
                                     course=course, createtime=createtime)
            except:
                return HttpResponse(json.dumps({'code': 1, 'msg': '顺序不能重复'}, ensure_ascii=False))

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
            jstime = request.POST.get('jstime', ' ')  # job salary调查时间
            difficult = request.POST.get('difficult', 4)
            totaltime = request.POST.get('totaltime', ' ')
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            sequence = request.POST.get('sequence')

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
                       sequence=sequence,
                       difficult=difficult, pathimg=pathimg, totaltime=totaltime, createtime=createtime)
            sql.save()
            return HttpResponse(json.dumps({'code': 0, 'msg': u'创建路线成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getcourse(request):
    """获取课程详细信息, 以及该课程下面所有的视频"""
    try:
        cid = request.GET.get('cid')
        course = Course.objects.get(id=cid)
        videos = Video.objects.filter(course=course).all().values()
        print course, videos
        return render(request, 'du/courselist.html', {'course': course, 'videos': videos})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getpath(request):
    """获取学习路线详细信息, 学习路线下包含的所有课程
        path为path对象, courseall包含所有的course对象
    """
    try:
        pid = request.GET.get('id')
        path = Path.objects.get(id=pid)
        sequence = path.sequence
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
        vps = Program.objects.all().values()
        try:
            techobj = Program.objects.get(name=type)
            courses = Course.objects.filter(tech=techobj).values('id')
        except:
            courses = Course.objects.filter().values('id')
            techobj = ''
        for c in courses:
            sql_pub = "select vc.*, vv.vtype, vv.id as video_id, vv.sequence, vp.name as vp_name, vp.color as vp_color from vcourse_program as vp, vcourse_course as vc, vcourse_video as vv where vp.id=vc.tech_id and vv.course_id=vc.id and vc.id=%s order by sequence limit 1" % \
                      c['id']
            ret = dictfetchall(sql_pub)
            if len(ret) != 0:
                pubs.append(ret[0])
            else:
                not_pubs.append(Course.objects.get(id=c['id']))
        return render(request, 'course_library.html',
                      {'pubs': pubs, 'not_pubs': not_pubs, 'vps': vps, 'tech_obj': techobj,
                       'xingxing': [0, 1, 2, 3, 4]})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def getpaths(request):
    """获取所有的路线"""
    try:
        sql = "select id, name, pathimg, color from vcourse_path"
        paths = dictfetchall(sql)
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
        sequence = path.sequence
        if UserPath.objects.filter(user=user, path=path).exists():
            User.objects.filter(id=uid).update(pathid=pid)
            sql = """select * from (select vv.vtype, vv.name, vv.sequence, vv.id, vv.course_id, vv.vtype_url, vw.createtime from vcourse_video as vv left join vrecord_watchrecord as vw on vv.id=vw.video_id and vw.user_id=%s where  vv.course_id in (%s) order by vw.createtime desc,vv.sequence asc) as t group by t.course_id order by t.createtime desc limit 1""" % (
                uid, sequence)
            video = dictfetchall(sql)[0]
            url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
            return HttpResponseRedirect(url)
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            UserPath.objects.create(user=user, path=path, createtime=t)
            User.objects.filter(id=uid).update(pathid=pid)
            seq = path.sequence
            course = seq.split(',')[0]
            sql = 'select id, sequence, vtype from vcourse_video where course_id =%s order by sequence limit 1' % course
            video = dictfetchall(sql)[0]
            url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
            return HttpResponseRedirect(url)
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))

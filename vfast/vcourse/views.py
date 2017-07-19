#!encoding:utf-8
import logging, traceback
import json
import time

from vfast.api import require_role, require_login, dictfetchall
from vuser.models import User
from vcourse.models import Technology, Course, Video, Path, UserPath, Section
from vrecord.models import WatchRecord
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def test(request):
    w = WatchRecord.objects.filter(id=1).values('user__username')
    #print w.query
    #print w
    from vpractice.models import Replay
    r = Replay.objects.filter(id=1).values('question__user__username')
    #print r.query
    #print r
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
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def getcourses(request):
    """获取所有的课程"""
    try:
        type = request.GET.get('type', None)
        vps = Technology.objects.all().values()
        if type:
            techobj = Technology.objects.get(name=type)
            pubs = Course.objects.filter(tech=techobj, pubstatus=0).values('id','name','desc','totaltime','difficult','icon','color','tech__color', 'tech__name')
            not_pubs = Course.objects.filter(tech=techobj, pubstatus=1).values('id','name','desc','totaltime','difficult','icon','color','tech__color', 'tech__name', 'pubdate')
        else:
            techobj = ''
            pubs = Course.objects.filter(pubstatus=0).values('id','name','desc','totaltime','difficult','icon','color','tech__color', 'tech__name')
            not_pubs = Course.objects.filter(pubstatus=1).values('id','name','desc','totaltime','difficult','icon','color','tech__color', 'tech__name','pubdate')
        return render(request, 'course_library.html',
                      {'pubs': pubs, 'not_pubs': not_pubs, 'vps': vps, 'tech_obj': techobj,
                       'xingxing': [0, 1, 2, 3, 4]})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def getpaths(request):
    """获取所有的路线"""
    try:
        paths = Path.objects.all()
        return render(request, 'learning_path.html', {'paths': paths})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


@require_login()
def join_path(request):
    try:
        pid = request.GET.get('pid')
        uid = request.session['user']['id']
        user = User.objects.get(id=uid)
        path = Path.objects.get(id=pid)
        sequence = path.p_sequence.split(',')
        User.objects.filter(id=uid).update(pathid=pid)
        if UserPath.objects.filter(user=user, path=path).exists():
            video = WatchRecord.objects.filter(user=user, course_id__in=sequence).order_by('-createtime').values(
                'video_id', 'video__vtype', 'createtime').first()
            logging.getLogger().info(video)
            if video:
                url = '/video/%s' % video['video_id'] if video['video__vtype'] == 0 else '/practice/%s' % video['video_id']
            else:
                course_id = sequence[0]
                video = Video.objects.filter(course_id=course_id, sequence=1).values('vtype', 'id').first()
                url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
            return HttpResponseRedirect(url)
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            UserPath.objects.create(user=user, path=path, createtime=t)
            course_id = sequence[0]
            video = Video.objects.filter(course_id=course_id, sequence=1).values('vtype', 'id').first()
            url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
            return HttpResponseRedirect(url)
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def course_detail(request):
    try:
        cid = request.GET.get('cid')
        course = Course.objects.get(id=cid)
        sections = Section.objects.filter(course=course).values()  # 课程下面所有的章节
        videos_course = Video.objects.filter(course_id=cid).count()  # 课程下所有的视频
        try:
            flag = False  # flag标记为开始学习,继续学习, True为继续学习
            uid = request.session['user']['id']
            # 课程下面用户观看完成的视频
            videos_watched = WatchRecord.objects.filter(course_id=cid, user_id=uid, status=0).values('status',
                                                                                                     'video_id',
                                                                                                     'createtime')
            for section in sections:
                videos_section = Video.objects.filter(section_id=section['id']).values()
                tmp = 0
                for v_section in videos_section:  # video_section
                    for v_watched in videos_watched:  # video_watched
                        if v_section['id'] == v_watched['video_id'] and v_watched['status'] == 0:
                            v_section['status'] = v_watched['status']
                            tmp += 1
                            break
                    if not v_section.has_key('status'):
                        v_section['status'] = 2
                    section['videos'] = videos_section
                    if tmp / videos_section.count() == 1:
                        section['process'] = u'已完成'
                    else:
                        section['process'] = '%s/%s' % (tmp, videos_section.count())
            video = WatchRecord.objects.filter(course_id=cid, user_id=uid).order_by('-createtime').values('video_id',
                                                                                                          'video__vtype',
                                                                                                          'createtime').first()
            if video:
                flag = True
                url = '/video/%s' % video['video_id'] if video['video__vtype'] == 0 else '/practice/%s' % video[
                    'video_id']
            else:
                v = Video.objects.filter(course_id=cid, sequence=1).values().first()        #如果课程下面没有视频会抛出异常
                url = '/video/%s' % v['id'] if v['vtype'] == 0 else '/practice/%s' % v['id']
            course_process = '%s/%s' % (videos_watched.count(), videos_course)
            jindu = videos_watched.count() / 1.0 / videos_course
            jindu = '%.2f%%' % (jindu * 100)
            return render(request, 'course_detail.html', {'sections': sections, 'course': course,
                                                          'course_process': course_process, 'flag': flag, 'url': url,
                                                          'xingxing': [0, 1, 2, 3, 4], 'jindu': jindu})
        except KeyError:
            #print 'wei denglu '
            for section in sections:
                videos_section = Video.objects.filter(section_id=section['id'])
                section['videos'] = videos_section
                section['process'] = '0/%s' % videos_section.count()
            return render(request, 'course_detail.html',
                          {'sections': sections, 'course': course, 'course_process': '0/%s' % videos_course,
                           'xingxing': [0, 1, 2, 3, 4], 'jindu': '0%'})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(status=404)

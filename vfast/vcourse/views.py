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
        for c in courses:
            sql_pub = "select vc.*, vv.vtype, vv.id as video_id, vv.sequence, vt.name as vt_name, vt.color as vt_color from vcourse_technology as vt, vcourse_course as vc, vcourse_video as vv where vt.id=vc.tech_id and vv.course_id=vc.id and vc.id=%s order by sequence limit 1" % \
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
        paths = Path.objects.all()
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
            url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
            return HttpResponseRedirect(url)
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


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
                for v_section in videos_section:
                    for v_watched in videos_watched:
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
                v = Video.objects.filter(course_id=cid, sequence=1).values().first()
                url = '/video/%s' % v['id'] if v['vtype'] == 0 else '/practice/%s' % v['id']
            if videos_watched.count() / videos_course == 1:
                course_process = u'已完成'
            else:
                course_process = '%s/%s' % (videos_watched.count(), videos_course)
            return render(request, 'course_detail.html', {'sections': sections, 'course': course,
                                                          'course_process': course_process, 'flag': flag, 'url': url,
                                                          'xingxing': [0, 1, 2, 3, 4]})
        except KeyError:
            for section in sections:
                videos_section = Video.objects.filter(section_id=section['id'])
                section['video'] = videos_section
                section['process'] = '0/%s' % videos_section.count()
            return render(request, 'course_detail.html',
                          {'sections': sections, 'course': course, 'course_process': '0/%s' % videos_course,
                           'xingxing': [0, 1, 2, 3, 4]})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(status=404)

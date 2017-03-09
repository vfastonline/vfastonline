#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from vuser.models import User
from vperm.models import Role
from vcourse.models import Path, Course, Video
from vrecord.models import WatchCourse, WatchRecord
from vgrade.api import headimg_urls
from vfast.api import encry_password, send_mail, get_validate, time_comp_now, dictfetchall
from django.db import connection

import json
import logging
import traceback
import base64
import time
import random


# Create your views here.
def test(request):
    return HttpResponse('hello,world~!')


def userexists(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            if email:
                retemail = User.objects.filter(email=email).exists()
                if retemail:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'邮箱已注册'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'还未注册'}, ensure_ascii=False))
            else:
                retusername = User.objects.filter(username=username).exists()
                if retusername:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'用户名已使用'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'还未注册'}, ensure_ascii=False))
        else:
            return render(request, 'du/usertest.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(u'服务器错误')


def register(request):
    try:
        if request.method == 'GET':
            return render(request, 'du/register.html')
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if (email and password):
                password = encry_password(password)
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'参数错误'}))

            program_exp = request.POST.get('program_exp', '')
            comp_use_time_day = request.POST.get('comp_use_time_day', '')
            into_it = request.POST.get('into_it', '')
            learn_habit = request.POST.get('learn_habit', '')
            sex = request.POST.get('sex', '')

            role = Role.objects.get(rolename='student')  # 取角色表里面普通用户的name
            headimg = random.choice(headimg_urls())
            active = base64.b64encode('%s|%s|%s' % (email, settings.SECRET_KEY, t)).strip()[:64]
            subject = u'智量酷账号激活'
            message = u'''
                                    恭喜您,注册智量酷账号成功!
                                    您的账号为: %s
                                    V-fast账号需要激活才能正常使用!
                                    点我激活账号

                                    如果无法点击请复制一下链接到浏览器地址
                                    %s/u/active?active=%s
                                ''' % (email, settings.HOST, active)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email, ])

            result = User.objects.get_or_create(email=email, username=username, password=password,
                                                program_exp=program_exp, createtime=t, sex=sex,
                                                comp_use_time_day=comp_use_time_day, into_it=into_it,
                                                learn_habit=learn_habit, active=active, role=role, headimg=headimg)
            if result:
                return HttpResponse(json.dumps({'code': 0, 'msg': u'注册成功, 请激活账号!'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'数据库错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}, ensure_ascii=False))


def useractive(request):
    try:
        active = request.GET.get('active', ' ')
        user = User.objects.get(active=active)
        if user:
            user.status = 1
            user.save()
            user = User.objects.filter(active=active, status=1).values(
                'email', 'id', 'role', 'username', 'totalscore', 'headimg', 'headimgframe').first()
            request.session['user'] = user
            request.session['login'] = True
            return HttpResponseRedirect('/')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'邮件已过期失效'}, ensure_ascii=False))


def resetpw(request):
    try:
        if request.method == 'GET':
            return render(request, 'du/usertest.html')
        else:
            email = request.POST.get('email', ' ')
            user = User.objects.filter(email=email).exists()
            if user:
                t = int(time.time())
                active = base64.b64encode('%s|%s' % (email, t)).strip()
                User.objects.filter(email=email).update(active=active)
                subject = u'智量酷用户账号密码重置'
                message = u'''
                            您在使用智量酷时点击了“忘记密码”链接，这是一封密码重置确认邮件。

您可以通过点击以下链接重置帐户密码:
%s/u/resetpw?active=%s
为保障您的帐号安全，请在24小时内点击该链接，您也可以将链接复制到浏览器地址栏访问。 若如果您并未尝试修改密码，请忽略本邮件，由此给您带来的不便请谅解。
本邮件由系统自动发出，请勿直接回复！

                                                ''' % (settings.HOST, active)
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email, ])
                return HttpResponse(json.dumps({'code': 0, 'msg': u'重置密码邮件已发送'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}, ensure_ascii=False))

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}))


def resetpwd_verify(request):
    try:
        if request.method == 'GET':
            active = request.GET.get('active')
            user = User.objects.get(active=active)
            return render(request, 'du/usertest.html', {'user': user})
        else:
            email = request.POST.get('email', ' ')
            password = request.POST.get('npw', ' ')
            password = encry_password(password)
            User.objects.filter(email=email).update(password=password)
            return HttpResponse('update password successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}))


def login(request):
    try:
        if request.method == 'GET':
            return render(request, 'login_left.html')
        else:
            email = request.POST.get('username', ' ')
            password = request.POST.get('password', ' ')
            password = encry_password(password)
            ret = User.objects.filter(Q(email=email) | Q(username=email), password=password, status=1).exists()
            if ret:
                # 账号登陆成功之后需要将用户的相关信息保存到session里面
                user = User.objects.filter(Q(email=email) | Q(username=email), password=password, status=1).values(
                    'email', 'id', 'role', 'username', 'totalscore', 'headimg', 'headimgframe', 'pathid').first()
                token = get_validate(email=user['email'], uid=user['id'], role=user['role'],
                                     fix_pwd=settings.SECRET_KEY)
                request.session['token'] = token
                request.session['user'] = user
                request.session['login'] = True
                # pre_url = request.session.get('pre_url', '/')
                pre_url = request.META.get('HTTP_REFERER')
                if len(pre_url.split('/')) == 2:
                    return HttpResponse(json.dumps({'code': 0, 'url': '/u/%s/' % user['id']}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'url': pre_url}, ensure_ascii=False))
            else:
                if User.objects.filter(Q(email=email) | Q(username=email), password=password, status=0).exists():
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'账号未激活'}, ensure_ascii=False))
                elif User.objects.filter(Q(email=email) | Q(username=email)).exists() == False:
                    return HttpResponse(json.dumps({'code': 2, 'msg': u'账号不存在'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 3, 'msg': u'密码错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 4, 'msg': u'服务器错误'}, ensure_ascii=False))


def userdetail(request):
    try:
        uid = request.session['user']['id']
        user = User.objects.filter(id=uid).values('totalscore', 'username', 'headimg', 'headimgframe')[0]
        return HttpResponse(json.dumps(user, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}))


def dashboard(request, param):
    try:
        param = int(param)
        user = User.objects.get(id=param)
        pathid = user.pathid
        # 当没有正在学习的路线的时候, 显示已经学过的课程
        if pathid == 0:
            sql = "select vr.video_id, vv.vtype as video_type, vc.*, vp.color as tech_color, vp.name as tech_name from vrecord_watchrecord as vr, vcourse_video as vv , vcourse_course as vc , vcourse_program as vp where vp.id=vc.tech_id and vr.user_id=%s and vr.video_id=vv.id and vr.course_id=vc.id GROUP BY id" % user.id
            courses = dictfetchall(sql)
            # return HttpResponse('ok')
            return render(request, 'dashBoard.html',
                          {'courses': courses, 'path_flag': False, 'xingxing': [0, 1, 2, 3, 4]})

        # 显示正在学习的路线
        else:
            path = Path.objects.get(id=pathid)
            sequence = path.sequence
            sql = 'select * from vcourse_course where id in  (%s) order by field (id, %s)' % (sequence, sequence)
            courses = dictfetchall(sql)  # 获取路线在的所有课程, sequence
            sql2 = 'select * from vrecord_watchcourse where user_id = %s AND course_id in (%s)' % (user.id, sequence)
            courses_wathced = dictfetchall(sql2)  # 获取用户观看过当前路线的课程,是否观看完成

            # 课程时间显示转换, 如果以看完课程,显示课程观看时间, 如果没有看完课程,显示课程总时间
            for item in courses:
                for j in courses_wathced:
                    if item['id'] == j['course_id']:
                        item['viewtime'] = time_comp_now(j['createtime'])
                if not item.has_key('viewtime'):
                    item['viewtime'] = item['totaltime']

                # 查找出用户观看过的视频
                sql3 = "select vv.*, t.createtime  from (select * from vrecord_watchrecord where user_id=%s and course_id=%s order by createtime desc limit 1) as t,vcourse_video as vv where vv.id = t.video_id" % (
                    user.id, item['id'])
                ret3 = dictfetchall(sql3)
                if len(ret3) == 1:
                    item['video_id'] = ret3[0]['id']
                    item['video_name'] = ret3[0]['name']
                    item['vtype_url'] = ret3[0]['vtype_url']
                    item['vtype'] = ret3[0]['vtype']
                    item['createtime'] = ret3[0]['createtime']
                else:
                    sql_video = "select * from vcourse_video where course_id =%s order by sequence limit 1;" % item[
                        'id']
                    ret_video = dictfetchall(sql_video)
                    item['video_id'] = ret_video[0]['id']
                    item['video_name'] = ret_video[0]['name']
                    item['vtype_url'] = ret_video[0]['vtype_url']
                    item['vtype'] = ret_video[0]['vtype']
                    item['createtime'] = 0  # 未观看视频, 跳转到course的第一个视频

            tmp = []
            for z in courses:
                tmp.append(z['createtime'])
            tmp.sort()
            maxdate = tmp.pop()
            for item in courses:
                if item['createtime'] == maxdate and maxdate != 0:
                    item['flag'] = 1
                    course_obj = Course.objects.get(id=item['id'])
                    len_v = Video.objects.filter(course=course_obj).__len__()
                    len_v_wathc = WatchRecord.objects.filter(course=course_obj, user=user).__len__()
                    item['viewtime'] = '%s/%s' % (len_v_wathc, len_v)
                    item['video_jindu'] = '%.2f%%' % ((len_v_wathc / 1.0 / len_v) * 100)
                    icon_url = item['icon_url'].split('.')
                    icon_url[0] = icon_url[0] + '_1'
                    icon_url = '.'.join(icon_url)
                    vicon_url = item['vtype_url'].split('.')
                    vicon_url[0] = vicon_url[0] + '_1'
                    vicon_url = '.'.join(vicon_url)
                    item['icon_url'] = icon_url
                    item['vtype_url'] = vicon_url
                else:
                    item['flag'] = 0

            # 进行路线的百分比
            p_num_sql = 'select count(1) as sum from vcourse_video where course_id in (%s)' % sequence
            v_num_sql = 'select COUNT(1) as sum from vrecord_watchrecord where course_id in  (%s) AND user_id = %s  AND status = 0' % (
                sequence, user.id)
            p_num = dictfetchall(p_num_sql)
            v_num = dictfetchall(v_num_sql)
            jindu = v_num[0]['sum'] / 1.0 / p_num[0]['sum']
            jindu = '%.2f%%' % (jindu * 100)
            return render(request, 'dashBoard.html',
                          {'courses': courses, 'jindu': jindu, 'path_flag': True, 'path_name': path.name})

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(u'页面错误')

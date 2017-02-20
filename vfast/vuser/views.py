#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from vuser.models import User
from vperm.models import Role
from vcourse.models import Path, Course
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
            print user.status
            user.save()
            user = User.objects.filter(active=active, status=1).values(
                'email', 'id', 'role', 'username', 'totalscore', 'headimg', 'headimgframe').first()
            print user
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
            return render(request, 'usertest.html')
        else:
            email = request.POST.get('username', ' ')
            password = request.POST.get('password', ' ')
            password = encry_password(password)
            print email, password
            ret = User.objects.filter(Q(email=email) | Q(username=email), password=password, status=1).exists()
            if ret:
                # 账号登陆成功之后需要将用户的相关信息保存到session里面
                user = User.objects.filter(Q(email=email) | Q(username=email), password=password, status=1).values(
                    'email', 'id', 'role', 'username', 'totalscore', 'headimg', 'headimgframe').first()
                print user['email']
                token = get_validate(email=user['email'], uid=user['id'], role=user['role'],
                                     fix_pwd=settings.SECRET_KEY)
                request.session['token'] = token
                request.session['user'] = user
                request.session['login'] = True
                pre_url = request.session.get('pre_url', '/')
                # print pre_url, email, password
                return HttpResponse(json.dumps({'code': 0, 'pre_url': pre_url}, ensure_ascii=False))
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
        if request.method == 'GET':
            uid = request.GET.get('uid', ' ')
            user = User.objects.filter(id=uid).values()[0]
            print user
            return HttpResponse(json.dumps(user, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}))


def logout(request):
    # 销毁session信息
    pass


def dashboard(request, param):
    try:
        param = int(param)
        user = User.objects.get(uniqeid=param)
        pathid = user.pathid
        orders = Path.objects.get(id=pathid).orders

        sql = 'select * from vcourse_course where id in  (%s) order by field (id, %s)' % (orders, orders)
        print sql
        courses = dictfetchall(sql)

        sql2 = 'select * from vrecord_watchcourse where user_id = %s' % user.id
        courses_wathced = dictfetchall(sql2)

        for i in courses:
            for j in courses_wathced:
                try:
                    if i['id'] == j['course_id']:
                        i['viewtime'] = time_comp_now(j['createtime'])
                    else:
                        i['viewtime'] = i['totaltime']
                except:
                    logging.getLogger().warning('dashboard, 匹配是否看完课程时候, keyerror错误')

        print courses

        sql3 = """select * from (select vw. *, vv.name from vrecord_watchrecord as vw, vcourse_video as vv where vw.video_id = vv.id and vw.course_id in (%s) and vw.user_id = %s order by vw.createtime desc) as t group by course_id;
""" % (orders, user.id)
        print sql3
        videos = dictfetchall(sql3)
        # print videos

        for cour in courses:
            for v in videos:
                if cour['id'] == v['course_id']:
                    cour['video_id'] = v['id']
                    cour['video_name'] = v['name']
        print courses

        for k in courses:
            k['createtime'] = int(time.mktime(time.strptime(k['createtime'], '%Y-%m-%d %H:%M:%S')))
        tmp = []
        for z in courses:
            tmp.append(z['createtime'])
        tmp.sort()
        maxdate = tmp.pop()
        for z in courses:
            if z['createtime'] == maxdate:
                z['flag'] = 1
            else:
                z['flag'] = 0
        logging.getLogger().info(connection.queries)
        return HttpResponse(json.dumps({'result': courses}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('failed')

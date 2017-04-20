#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q, Sum
from vuser.models import User, DailyTask, PtoP
from vperm.models import Role
from vcourse.models import Path, Course, Video
from vrecord.models import WatchRecord, Score
from vbadge.models import UserBadge
from vfast.api import encry_password, send_mail, get_validate, time_comp_now, dictfetchall
from vrecord.api import sum_score_tech

import os
import json
import logging
import traceback
import base64
import time


# Create your views here.
def test(request):
    begin = int(time.time())
    time.sleep(3)
    end = int(time.time())
    return render(request, 'test.html')


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
            headimg = '/static/head/defaultIMG.svg'
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
                'email', 'id', 'role', 'username', 'totalscore', 'headimg').first()
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
                    'email', 'id', 'role', 'username', 'totalscore', 'headimg', 'pathid').first()
                token = get_validate(email=user['email'], uid=user['id'], role=user['role'],
                                     fix_pwd=settings.SECRET_KEY)
                request.session['token'] = token
                request.session['user'] = user
                request.session['login'] = True
                pre_url = request.META.get('HTTP_REFERER')
                if pre_url.split('/')[3] == '':
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
        user = \
            User.objects.filter(id=uid).values('totalscore', 'username', 'headimg', 'intro',
                                               'githuburl',
                                               'personpage', 'location')[0]
        return HttpResponse(json.dumps(user, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}))


def dashboard(request, param):
    try:
        param = int(param)
        user = User.objects.get(id=param)
        # 当没有正在学习的路线的时候, 显示已经学过的课程
        if user.pathid == 0:
            sql = "select vr.video_id, vv.vtype as video_type, vc.*, vt.color as tech_color, vt.name as tech_name from vrecord_watchrecord as vr, vcourse_video as vv , vcourse_course as vc , vcourse_technology as vt where vt.id=vc.tech_id and vr.user_id=%s and vr.video_id=vv.id and vr.course_id=vc.id GROUP BY id" % user.id
            courses = dictfetchall(sql)
            task_create = task_daily(user)
            if task_create:
                flag, tasks = task_finish(user)  # 判断是否完成今日任务, 并返回
            else:
                flag, tasks = False, []
            print tasks
            print courses
            return render(request, 'dashBoard.html',
                          {'courses': courses, 'path_flag': False, 'xingxing': [0, 1, 2, 3, 4], 'flag': flag,
                           'tasks': tasks})
        # 显示正在学习的路线
        else:
            path = Path.objects.get(id=user.pathid)
            sequence = path.p_sequence
            sql = 'select * from vcourse_course where id in  (%s) order by field (id, %s)' % (sequence, sequence)
            courses = dictfetchall(sql)  # 获取路线在的所有课程, sequence
            sql2 = 'select * from vrecord_watchcourse where user_id = %s AND course_id in (%s)' % (user.id, sequence)
            courses_wathced = dictfetchall(sql2)  # 获取用户观看过当前路线的课程,是否观看完成

            # 课程时间显示转换, 如果以看完课程,显示课程观看时间, 如果没有看完课程,显示课程总时间
            for item in courses:
                for j in courses_wathced:
                    if item['id'] == j['course_id']:
                        item['viewtime'] = '%s%s' % (time_comp_now(j['createtime']), '完成')
                if not item.has_key('viewtime'):
                    item['viewtime'] = item['totaltime']

                # 查找出用户观看过的视频
                sql3 = "select vv.*, t.createtime  from (select * from vrecord_watchrecord where user_id=%s and course_id=%s order by createtime desc limit 1) as t,vcourse_video as vv where vv.id = t.video_id" % (
                    user.id, item['id'])
                ret3 = dictfetchall(sql3)
                if len(ret3) == 1:
                    item['video_id'] = ret3[0]['id']
                    item['video_name'] = ret3[0]['name']
                    # item['vtype_url'] = ret3[0]['vtype_url']
                    item['vtype'] = ret3[0]['vtype']
                    item['createtime'] = ret3[0]['createtime']
                else:
                    sql_video = "select * from vcourse_video where course_id =%s order by sequence limit 1;" % item[
                        'id']
                    ret_video = dictfetchall(sql_video)
                    item['video_id'] = ret_video[0]['id']
                    item['video_name'] = ret_video[0]['name']
                    # item['vtype_url'] = ret_video[0]['vtype_url']
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
                    len_v = Video.objects.filter(course=course_obj).count()
                    len_v_wathc = WatchRecord.objects.filter(course=course_obj, user=user, status=0).count()
                    item['viewtime'] = '%s/%s' % (len_v_wathc, len_v)
                    item['video_jindu'] = '%.2f%%' % ((len_v_wathc / 1.0 / len_v) * 100)
                else:
                    item['flag'] = 0
            # print courses
            # 进行路线的百分比
            p_num_sql = 'select count(1) as sum from vcourse_video where course_id in (%s)' % sequence
            v_num_sql = 'select COUNT(1) as sum from vrecord_watchrecord where course_id in  (%s) AND user_id = %s  AND status = 0' % (
                sequence, user.id)
            p_num = dictfetchall(p_num_sql)
            v_num = dictfetchall(v_num_sql)
            jindu = v_num[0]['sum'] / 1.0 / p_num[0]['sum']
            jindu = '%.2f%%' % (jindu * 100)

            task_create = task_daily(user)  # 检测推荐任务, 没有就创建
            if task_create:
                flag, tasks = task_finish(user)  # 判断是否完成今日任务, 并返回
            else:
                flag, tasks = False, []
            # print flag, tasks
            # courses 路线下所有的课程, jindu 路线进度, path_flag 显示路线, tasks 推荐任务, flag 今日任务是否完成
            return render(request, 'dashBoard.html',
                          {'courses': courses, 'jindu': jindu, 'path_flag': True, 'path_name': path.name,
                           'tasks': tasks, 'flag': flag})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(u'页面错误' + traceback.format_exc())


def task_daily(user):
    try:
        ret = WatchRecord.objects.filter(user=user).exists()
        d_ret = DailyTask.objects.filter(createtime__contains=time.strftime('%Y-%m-%d'),
                                         user_id=user.id).exists()
        if ret and not d_ret:
            sql = 'select vw.*, vv.sequence from vrecord_watchrecord as vw, vcourse_video as vv where user_id = %s and vw.video_id=vv.id order by createtime desc limit 1;' % user.id
            result = dictfetchall(sql)
            seqs = [str(result[0]['sequence'] + i) for i in range(1, 4)]
            sql_recommand = "select * from vcourse_video where course_id = %s and sequence in (%s)" % (
                result[0]['course_id'], ','.join(seqs))
            # print sql, seqs, sql_recommand
            recommand = dictfetchall(sql_recommand)
            if len(recommand) != 0:
                for item in recommand:
                    DailyTask.objects.create(user_id=user.id, video_id=item['id'], createtime=time.strftime('%Y-%m-%d'),
                                             vtime=item['vtime'], vtype=item['vtype'], video_name=item['name'])
                return True
        elif ret and d_ret:
            return True
        else:
            return False
    except:
        logging.getLogger().error(traceback.format_exc())
        return False


def task_finish(user):
    try:
        dt_all = DailyTask.objects.filter(user_id=user.id, createtime=time.strftime('%Y-%m-%d')).values().order_by(
            'video_id')
        wr = WatchRecord.objects.filter(user=user, createtime__contains=time.strftime('%Y-%m-%d'),
                                        status=0).values_list('video_id').order_by('video_id')
        dt = DailyTask.objects.filter(user_id=user.id, createtime=time.strftime('%Y-%m-%d')).values_list('video_id')
        for item in dt_all:
            for d in wr:
                # logging.getLogger().info(d)
                if item['video_id'] == d[0]:
                    item['status'] = 0
                    item['vtime'] = '已完成'
                    break
            if not item.has_key('status'):
                item['status'] = 1
        # print dt_all, wr
        if set(dt).issubset(set(wr)):
            if Score.objects.filter(user_id=user.id, score=10, createtime=time.strftime('%Y-%m-%d')).exists():
                return True, dt_all
            else:
                Score.objects.create(user_id=user.id, score=10, createtime=time.strftime('%Y-%m-%d'))
                user.totalscore += 10
                user.save()
                return True, dt_all
        else:
            return False, dt_all
    except:
        logging.getLogger().error(traceback.format_exc())
        return False, []


def follow_people(request):
    try:
        followed_id = request.GET.get('followed_id')  # 被关注人的ID
        type = request.GET.get('type')  # 1关注, 0取消关注
        try:
            follow_id = request.session['user']['id']  # 关注人的ID
        except ValueError:
            return HttpResponse(u'未登录')
        followed = User.objects.get(id=followed_id)
        follow = User.objects.get(id=follow_id)
        if not PtoP.objects.filter(follow=follow, followed=followed).exists() and type == '1':
            PtoP.objects.create(follow=follow, followed=followed)
            return HttpResponse(json.dumps({'code': 0, 'msg': '关注成功'}))
        elif PtoP.objects.filter(follow=follow, followed=followed).exists() and type == '0':
            PtoP.objects.filter(follow=follow, followed=followed).delete()
            return HttpResponse(json.dumps({'code': 0, 'msg': '取消关注成功'}))
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'follow_people interface normal'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def user_model(request):
    try:
        uid = request.GET.get('uid')
        tech_score = sum_score_tech(uid)
        user = \
            User.objects.filter(id=uid).values('totalscore', 'username', 'headimg', 'intro', 'githuburl', 'personpage',
                                               'location', 'githubrepo')[0]
        followid = request.session['user']['id']  # 关注人的ID
        followed_obj = User.objects.get(id=uid)  # 被关注人对象
        follow_obj = User.objects.get(id=followid)  # 关注人对象
        p2p_status = PtoP.objects.filter(follow=follow_obj, followed=followed_obj).exists()  # 是否关注
        badge_num = UserBadge.objects.filter(user=follow_obj).count()  # 模态窗扣弹出的 用户的勋章数量
        print uid, tech_score, user, p2p_status
        return HttpResponse(
            json.dumps({'user': user, 'badge': badge_num, 'tech_score': tech_score, 'guanzhu': p2p_status}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def person_page(request):
    try:
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponseRedirect('/')
        user_obj = User.objects.get(id=uid)
        tech_score = sum_score_tech(uid)
        sql = 'select vb.badgename, vb.badgeurl, vu.* from vbadge_userbadge as vu , vbadge_badge as vb where vu.user_id = %s and vu.badge_id = vb.id;' % uid
        badges = dictfetchall(sql)
        print badges
        sum_watch_video_time = WatchRecord.objects.filter(user=user_obj).aggregate(totaltime=Sum('video_time'))

        return render(request, 'personalCenter.html', {'user': user_obj, 'tech_score': tech_score, 'badges': badges,'badgesLen':len(badges),
                                                       'totaltime': sum_watch_video_time['totaltime']})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def is_open(request):
    try:
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponseRedirect('/')
        is_open = request.GET.get('is_open')
        print is_open
        User.objects.filter(id=uid).update(is_open=is_open)
        return HttpResponse('is_open update successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def change_headimg(request):
    try:
        if request.method == 'POST':
            headimg = request.FILES.get('headimg', None)
            uid = request.POST.get('uid',None)
            if not headimg:
                return HttpResponse('no headimg for upload!')
            destination = os.path.join(settings.MEDIA_ROOT, 'user_headimg')
            if not os.path.isdir(destination):
                os.mkdir(destination)
            print destination
            headfile = open(os.path.join(destination, headimg.name), 'wb')
            for chunk in headimg.chunks():
                headfile.write(chunk)
            headfile.close()
            user = User.objects.get(id=uid)
            user.headimg = '/media/user_headimg/%s' % headimg.name
            user.save()
            return HttpResponse(json.dumps({'headimg':'/media/user_headimg/%s' % headimg.name}))
        return HttpResponse('get method ok')

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def default_headimg(request):
    try:
        if request.method == 'POST':
            uid = request.POST.get('uid')
            user = User.objects.get(id=uid)
            user.headimg = '/static/head/defaultIMG.svg'
            user.save()
            return HttpResponse(json.dumps({'headimg':'/static/head/defaultIMG.svg'}))
        else:
            return HttpResponse('Please use post method')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def github(request):
    try:
        if request.method == 'GET':
            uid = request.GET.get('uid')
            status = request.GET.get('status')
            print uid, status
            if status == 'on':
                return HttpResponseRedirect('/github_login')
        else:
            return HttpResponse('method error!')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())
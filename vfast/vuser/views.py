#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q, Sum
from vuser.models import User, DailyTask, PtoP, DailyTaskstatus, Userplan
from vperm.models import Role
from vcourse.models import Path, Course, Video
from vrecord.models import WatchRecord, Score
from vbadge.models import UserBadge
from vfast.api import encry_password, get_validate, time_comp_now, dictfetchall, require_login, get_day_of_day
from vrecord.api import sum_score_tech
from vuser.api import *
from vcourse.api import track_process
from vfast.error_page import *

import os
import json
import logging
import traceback
import base64
import time
import random


# Create your views here.
def test(request):
    return render(request, 'inspectdetail.html')


def userexists(request):
    """判断email, nickname是否存在"""
    try:
        if request.method == 'POST':
            phone = request.POST.get('phone', None)
            nickname = request.POST.get('nickname', None)
            if phone:
                retphone = User.objects.filter(phone=phone).exists()
                if retphone:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'手机号已注册'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'手机号还未注册'}, ensure_ascii=False))
            else:
                retnickname = User.objects.filter(nickname=nickname).exists()
                if retnickname:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'用户名已使用'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'还未注册'}, ensure_ascii=False))
        else:
            return render(request, 'du/usertest.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def register(request):
    """用户注册"""
    try:
        if request.method == 'GET':
            return render(request, 'du/register.html')
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            nickname = request.POST.get('nickname', None)
            password = request.POST.get('password', None)
            phone = request.POST.get('phone', None)
            password = encry_password(password)

            program_exp = request.POST.get('program_exp', '')
            comp_use_time_day = request.POST.get('comp_use_time_day', '')
            into_it = request.POST.get('into_it', '')
            learn_habit = request.POST.get('learn_habit', '')
            sex = request.POST.get('sex', '')

            role = Role.objects.get(rolename='student')  # 取角色表里面普通用户的name
            headimg = '/static/head/defaultIMG.svg'
            user_exists = User.objects.filter(phone=phone).exists()
            if user_exists:
                return HttpResponse(json.dumps({'code': 3, 'msg': u'用户已存在,请登录'}, ensure_ascii=False))
            result = User.objects.create(phone=phone, nickname=nickname, password=password, totalscore=10,
                                         program_exp=program_exp, createtime=t, sex=sex,
                                         comp_use_time_day=comp_use_time_day, into_it=into_it,
                                         learn_habit=learn_habit, role=role, headimg=headimg)
            if result:
                user = User.objects.filter(phone=phone).values(
                    'phone', 'id', 'role', 'nickname', 'totalscore', 'headimg').first()
                logging.getLogger().info(user)
                request.session['user'] = user
                request.session['login'] = True
                return HttpResponse(json.dumps({'code': 0, 'msg': u'注册成功'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'数据库错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def phone_code(request):
    """用户手机注册"""
    try:
        if request.method == "POST":
            phone = request.POST.get('phone')
            code = ''
            for i in range(4):
                code += str(random.randint(0, 9))
            from vfast.api import sendmessage
            try:
                sendmessage(phone, {'code': code})
                logging.getLogger().info(u'注册验证码短信发送成功')
                import hashlib
                code = hashlib.new('md5', code).hexdigest()
                return HttpResponse(json.dumps({'code': 0, 'phone_code': code}))
            except:
                logging.getLogger().error(u'注册短信发送失败')
                return HttpResponse(json.dumps({'code': 1, 'msg': u'注册短信验证码发送失败'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def reset_password(request):
    """重置密码"""
    try:
        if request.method == 'POST':
            uid = request.session['user']['id']
            password = request.POST.get('password')
            password = encry_password(password)
            User.objects.filter(id=uid).update(password=password)
            return HttpResponse(json.dumps({'code': 0}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def login(request):
    """用户登录"""
    try:
        if request.method == 'GET':
            return render(request, 'login_left.html')
        else:
            phone = request.POST.get('phone', ' ')
            password = request.POST.get('password', ' ')
            password = encry_password(password)
            ret = User.objects.filter(Q(phone=phone) | Q(nickname=phone), password=password).exists()
            if ret:
                # 账号登陆成功之后需要将用户的相关信息保存到session里面
                user = User.objects.filter(Q(phone=phone) | Q(nickname=phone), password=password).values(
                    'phone', 'id', 'role', 'nickname', 'totalscore', 'headimg', 'pathid').first()
                token = get_validate(email=user['phone'], uid=user['id'], role=user['role'],
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
                if User.objects.filter(Q(phone=phone) | Q(nickname=phone)).exists() == False:
                    return HttpResponse(json.dumps({'code': 2, 'msg': u'账号不存在'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 3, 'msg': u'密码错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def userdetail(request):
    """用户详情"""
    try:
        uid = request.session['user']['id']
        user = \
            User.objects.filter(id=uid).values('totalscore', 'nickname', 'headimg', 'intro',
                                               'githuburl',
                                               'personpage')[0]
        return HttpResponse(json.dumps(user, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}))


def dashboard(request, param):
    """个人Dashboard页面"""
    try:
        param = int(param)
        user = User.objects.get(id=param)
        # 显示已经学过的或者正在学习的课程
        sql = "select vr.video_id, vv.vtype as video_type, vc.*, vt.color as tech_color, vt.name as tech_name from vrecord_watchrecord as vr, vcourse_video as vv , vcourse_course as vc , vcourse_technology as vt where vt.id=vc.tech_id and vr.user_id=%s and vr.video_id=vv.id and vr.course_id=vc.id GROUP BY id" % user.id
        courses_learning = dictfetchall(sql)
        task_create = task_daily(user)
        if task_create:
            flag, tasks = task_finish(user)  # 判断是否完成今日任务, 并返回
        else:
            flag, tasks = False, []
        if user.pathid == 0:
            pass

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
                    item['vtype'] = ret3[0]['vtype']
                    item['createtime'] = ret3[0]['createtime']
                else:
                    sql_video = "select * from vcourse_video where course_id =%s order by sequence limit 1;" % item[
                        'id']
                    ret_video = dictfetchall(sql_video)
                    if len(ret_video) == 0:
                        # 如果添加了课程,但是没有为课程添加视频, 默认读取第一个视频
                        sql_v = 'select * from vcourse_video limit 1'
                        ret_sql_v = dictfetchall(sql_v)
                        item['video_id'] = ret_sql_v[0]['id']
                        item['vtype'] = ret_sql_v[0]['vtype']
                        item['createtime'] = 0
                        item['video_name'] = ret_sql_v[0]['name']
                    else:
                        item['video_id'] = ret_video[0]['id']
                        item['video_name'] = ret_video[0]['name']
                        item['vtype'] = ret_video[0]['vtype']
                        item['createtime'] = 0  # 未观看视频, 跳转到course的第一个视频
            tmp = []
            for z in courses:
                tmp.append(str(z['createtime']))
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
            # 进行路线的百分比
            jindu, jindu_2 = track_process(user.id, sequence)
            return render(request, 'dashBoard.html',
                          {'courses_path': courses, 'jindu': jindu, 'path_name': path.name,
                           'courses': courses_learning, 'xingxing': [0, 1, 2, 3, 4],
                           'tasks': tasks, 'flag': flag})

        return render(request, 'dashBoard.html',
                      {'courses': courses_learning, 'path_flag': False, 'xingxing': [0, 1, 2, 3, 4], 'flag': flag,
                       'tasks': tasks})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def task_daily(user):
    """创建每日任务"""
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
            recommand = dictfetchall(sql_recommand)
            if len(recommand) != 0:
                for item in recommand:
                    DailyTask.objects.create(user_id=user.id, video_id=item['id'], createtime=time.strftime('%Y-%m-%d'),
                                             vtime=item['vtime'], vtype=item['vtype'], video_name=item['name'])
                DailyTaskstatus.objects.create(user_id=user.id, createtime=time.strftime('%Y-%m-%d'), taskstatus=1)
                return True
        elif ret and d_ret:
            return True
        else:
            return False
    except:
        logging.getLogger().error(traceback.format_exc())
        return False


def task_finish(user):
    """每日任务是否完成"""
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
        # #print dt_all, wr
        if set(dt).issubset(set(wr)):
            if DailyTaskstatus.objects.filter(user_id=user.id, createtime=time.strftime('%Y-%m-%d'), taskstatus=0):
                return False, dt_all
            else:
                Score.objects.create(user_id=user.id, score=10, createtime=time.strftime('%Y-%m-%d'))
                user.totalscore += 10
                user.save()
                DailyTaskstatus.objects.filter(user_id=user.id, createtime=time.strftime('%Y-%m-%d')).update(
                    taskstatus=0)
                return True, dt_all
        else:
            return False, dt_all
    except:
        logging.getLogger().error(traceback.format_exc())
        return False, []


def follow_people(request):
    """关注功能"""
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
            return HttpResponse(json.dumps({'code': 0, 'msg': '取消关注成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'follow_people interface normal'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def user_model(request):
    """用户弹窗"""
    try:
        uid = request.GET.get('uid')
        tech_score = sum_score_tech(uid)
        user = \
            User.objects.filter(id=uid).values('totalscore', 'nickname', 'headimg', 'intro', 'githuburl', 'personpage',
                                               'city', 'githubrepo')[0]
        followid = request.session['user']['id']  # 关注人的ID
        followed_obj = User.objects.get(id=uid)  # 被关注人对象
        follow_obj = User.objects.get(id=followid)  # 关注人对象
        p2p_status = PtoP.objects.filter(follow=follow_obj, followed=followed_obj).exists()  # 是否关注
        badge_num = UserBadge.objects.filter(user=follow_obj).count()  # 模态窗扣弹出的 用户的勋章数量
        # print uid, tech_score, user, p2p_status
        return HttpResponse(
            json.dumps({'user': user, 'badge': badge_num, 'tech_score': tech_score, 'guanzhu': p2p_status}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


@require_login()
def person_page(request):
    """个人中心页面"""
    try:
        uid = request.session['user']['id']
        user_obj = User.objects.get(id=uid)
        tech_score = sum_score_tech(uid)
        sql = 'select vb.badgename, vb.small_url, vu.* from vbadge_userbadge as vu , vbadge_badge as vb where vu.user_id = %s and vu.badge_id = vb.id;' % uid
        print sql
        badges = dictfetchall(sql)
        # print badges
        sum_watch_video_time = WatchRecord.objects.filter(user=user_obj).aggregate(totaltime=Sum('video_time'))

        return render(request, 'personalCenter.html',
                      {'user': user_obj, 'tech_score': tech_score, 'badges': badges, 'badgesLen': len(badges),
                       'totaltime': sum_watch_video_time['totaltime']})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def editpage(request):
    """个人编辑页面"""
    try:
        if request.method == 'GET':
            uid = request.session['user']['id']
            user = User.objects.get(id=uid)
            # return render(request, 'editInfo.html', {'user': user})
            return render(request, 'personedit.html', {'user': user})
        else:
            return HttpResponse(u'请求错误')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def is_open(request):
    """用户信息是否公开"""
    try:
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponseRedirect('/')
        is_open = request.GET.get('is_open')
        # print is_open
        User.objects.filter(id=uid).update(is_open=is_open)
        return HttpResponse('is_open update successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def change_headimg(request):
    """修改个人头像呢"""
    try:
        if request.method == 'POST':
            headimg = request.FILES.get('headimg', None)
            uid = request.POST.get('uid', None)
            if not headimg:
                return HttpResponse('no headimg for upload!')
            destination = os.path.join(settings.MEDIA_ROOT, 'user_headimg')
            if not os.path.isdir(destination):
                os.system('mkdir -p %s ' % destination)
            # print destination
            user = User.objects.get(id=uid)
            filename = str(user.id) + '_' + time.strftime('%y%m%d') + '.jpg'
            logging.getLogger().error(filename)
            headfile = open(os.path.join(destination, filename), 'wb')
            for chunk in headimg.chunks():
                headfile.write(chunk)
            headfile.close()

            user.headimg = '/media/user_headimg/%s' % filename
            user.save()
            return HttpResponse(json.dumps({'headimg': '/media/user_headimg/%s' % filename}))
        return HttpResponse('get method ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def default_headimg(request):
    """恢复默认"""
    try:
        if request.method == 'POST':
            uid = request.session['user']['id']
            user = User.objects.get(id=uid)
            user.headimg = '/static/head/defaultIMG.svg'
            user.save()
            return HttpResponse(json.dumps({'headimg': '/static/head/defaultIMG.svg'}))
        else:
            return HttpResponse('Please use post method')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def github(request):
    """绑定github账号"""
    try:
        if request.method == 'GET':
            uid = request.session['user']['id']
            status = request.GET.get('status')
            # print uid, status
            if status == 'on':
                # print 'jihuo github zhanghao ~!'
                return HttpResponseRedirect('/github_login')
            else:
                user = User.objects.get(id=uid)
                user.githuburl = ''
                user.githubrepo = ''
                user.save()
                return HttpResponse(json.dumps({'code': 0, 'msg': 'github not link successful'}))
        else:
            return HttpResponse('method error!')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def personpage(request):
    """绑定个人主页"""
    try:
        if request.method == 'POST':
            uid = request.session['user']['id']
            homepage = request.POST.get('personpage')
            User.objects.filter(id=uid).update(personpage=homepage)
            return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def user_phone(request):
    """修改个人手机号码, 修改个人账号"""
    try:
        if request.method == 'POST':
            uid = request.session['user']['id']
            phone = request.POST.get('phone')
            User.objects.filter(id=uid).update(phone=phone)
            return HttpResponse(json.dumps({'code': 0}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def nikcname(request):
    """修改用户昵称"""
    try:
        if request.method == 'POST':
            nickname = request.POST.get('nickname')
            uid = request.session['user']['id']
            try:
                User.objects.filter(id=uid).update(nickname=nickname)
                return HttpResponse(json.dumps({'code': 0}))
            except:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'昵称重复'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def editelse(request):
    """用户编辑页面修改"""
    try:
        if request.method == 'POST':
            realname = request.POST.get('realname')
            birthday = request.POST.get('birthday')
            city = request.POST.get('city')
            intro = request.POST.get('intro')
            expect_job = request.POST.get('expect_job')
            expect_level = request.POST.get('expect_level')
            email = request.POST.get('email')
            current_company = request.POST.get('current_company')
            company_gangwei = request.POST.get('company_gangwei')
            uid = request.session['user']['id']
            User.objects.filter(id=uid).update(email=email, realname=realname, birthday=birthday, city=city,
                                               intro=intro,
                                               expect_job=expect_job, expect_level=expect_level,
                                               current_company=current_company,
                                               company_gangwei=company_gangwei)
            return HttpResponse(json.dumps({'code': 0, 'msg': 'successfully'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def userimage(request):
    try:
        if request.method == "POST":
            image = request.POST.get('image')
            ret = Detect(image)
            if ret:
                return HttpResponse(json.dumps({'code': 0, 'msg': 'ok'}))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': 'disapper'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def ucenter(request):
    """学员列表页面"""
    try:
        # if request.session['user']['role'] != 2:
        #     return HttpResponse(status=403)
        yesterday = get_day_of_day(n=-1)
        today = time.strftime('%Y-%m-%d')
        users = User.objects.filter(role_id=1).values('id', 'nickname', 'realname', 'pathid')
        for user in users:
            user['score'] = get_score_yesterday(user['id'], yesterday)
            user['vtime'] = get_videotime_yesterday(user['id'], yesterday)
            user['newcourse'] = get_newer_course(user['id'])
            user['t_yesterday'] = get_timu_status(user['id'], yesterday)
            user['t_average'] = get_timu_status(user['id'])
            user['studyplan'] = get_studyplan_status(user['id'], today)
            if user['pathid'] == 0:
                user['track_process'] = '未加入任何路线'
                user['track_name'] = '未加入任何路线'
            else:
                pobj = Path.objects.get(id=user['pathid'])
                sequence = pobj.p_sequence
                pathname = pobj.name
                user['track_process'] = track_process(user['id'], sequence=sequence)[0]
                user['track_name'] = pathname
        return render(request, 'xueyuanliebiao.html', {'users': users})
    except:
        logging.getLogger().error(traceback.format_exc())
        return page_error(request)


def uinfo(request):
    """学员昨日学习详情页面"""
    try:
        uid = request.GET.get('uid', None)
        if uid:
            yesterday = get_day_of_day(n=-1)
            user = User.objects.filter(id=uid).values('id', 'nickname', 'realname', 'pathid').first()
            user['score'] = get_score_yesterday(user['id'], yesterday)
            user['vtime'] = get_videotime_yesterday(user['id'], yesterday)
            user['newcourse'] = get_newer_course(user['id'])
            user['t_yesterday'] = get_timu_status(user['id'], yesterday)
            user['t_average'] = get_timu_status(user['id'])
            if user['pathid'] == 0:
                user['track_process'] = '未加入任何路线'
                user['track_name'] = '未加入任何路线'
            else:
                pobj = Path.objects.get(id=user['pathid'])
                sequence = pobj.p_sequence
                pathname = pobj.name
                user['track_process'] = track_process(user['id'], sequence=sequence)[0]
                user['track_name'] = pathname
            return render(request, 'uinfo.html', {'user':user})
        else:
            return page_not_found(request)
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def uplan(request):
    """学员计划"""
    try:
        if request.method == "POST":
            uid = request.POST.get('uid', None)
            print uid
            if not uid:
                return HttpResponse(json.dumps({'code': 2, 'msg': '参数不正确'}, ensure_ascii=False))
            plan_desc = request.POST.get('plan_desc')
            opinion = request.POST.get('opinion')
            nums = request.POST.get('nums')
            createtime = get_day_of_day(n=1)
            Userplan.objects.create(plan_desc=plan_desc, createtime=createtime, nums=nums, opinion=opinion, userid=uid,
                                    status=1)
            return HttpResponse(json.dumps({'code':0}))
        else:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请使用post method'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128, 'msg': '请求错误', 'error':traceback.format_exc()}))

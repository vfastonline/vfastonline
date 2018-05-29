#!encoding:utf-8
import logging
import os
import random
import time
import traceback

from django.conf import settings
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect

from vbadge.models import UserBadge
from vcourse.api import track_process
from vcourse.models import Path, Course, Skill
from vfast.api import encry_password, get_validate, time_comp_now, require_login, get_day_of_day, sendmessage
from vfast.error_page import *
from vperm.models import Role
from vrecord.api import sum_score_tech
from vrecord.models import WatchCourse
from vrecord.models import WatchRecord, Score
from vuser.api import *
from vuser.models import User, DailyTask, PtoP, DailyTaskstatus, Userplan
from vuser.skill_mastery_level import statistics_skill_mastery_level_by_path
from vresume.models import Resume


# Create your views here.
def test(request):
    # skill = Skill.objects.all().values()
    # for item in skill:
    #     print item
    return render(request, 'xinxicaiji.html')

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
            try:
                sendmessage(phone, {'code': code})
                logging.getLogger().info(u'验证码短信发送成功')
                import hashlib
                code = hashlib.new('md5', code).hexdigest()
                return HttpResponse(json.dumps({'code': 0, 'phone_code': code}))
            except:
                logging.getLogger().error(u'短信验证码发送失败')
                return HttpResponse(json.dumps({'code': 1, 'msg': u'短信验证码发送失败'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def forget_pwd_phone(request):
    """忘记密码检测电话号码"""
    try:
        if request.method == "POST":
            codetimes = request.session.setdefault('codetimes', 0)
            codetimes = 0
            phone = request.POST.get('phone', None)
            user = User.objects.filter(phone=phone).values().first()
            if user:
                if codetimes < 3:
                    request.session['phone'] = phone
                    code = ''
                    for i in range(4):
                        code += str(random.randint(0, 9))
                    User.objects.filter(phone=phone).update(code=code)
                    sendmessage(phone, {'code': code})
                    request.session['codetimes'] += 1
                    return HttpResponse(json.dumps({'code': 0, 'url': '/u/newpasswd'}))
                else:
                    return HttpResponse(json.dumps({'code': 1, 'msg': '该手机号今天发送验证码已超过三次'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 2, 'msg': '您还不是智量酷用户,请先注册'}, ensure_ascii=False))
        else:
            return render(request, 'wangjimima.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128, 'msg': '验证码发送失败'}, ensure_ascii=False))


def forget_pwd_reset(request):
    """通过忘记密码设置新密码"""
    try:
        if request.method == "POST":
            phone = request.session['phone']
            code = request.POST.get('code')
            passwd = request.POST.get('password')
            password = encry_password(password=passwd)
            user = User.objects.filter(phone=phone).values('phone', 'id', 'role', 'nickname', 'totalscore', 'headimg',
                                                           'pathid', 'code').first()
            if user['code'] == code:
                User.objects.filter(phone=phone).update(password=password)
                request.session['login'] = True
                request.session['user'] = user
                return HttpResponse(json.dumps({'code': 0, 'url': '/u/%s' % user['id']}))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': '验证码错误'}))
        else:
            return render(request, 'reset_passwprd.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


@require_login()
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
                    # return HttpResponse(json.dumps({'code': 0, 'url': '/u/%s/' % user['id']}, ensure_ascii=False))
                    return HttpResponse(json.dumps({'code': 0, 'url': '/u/person'}, ensure_ascii=False))
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
        today = time.strftime('%Y-%m-%d')
        user = User.objects.get(id=param)
        userplan = Userplan.objects.filter(userid=user.id, createtime=today).values().first()
        # 显示已经学过的或者正在学习的课程
        sql = "select vr.video_id, vv.vtype as video_type, vc.*, vt.color as tech_color, vt.name as tech_name from vrecord_watchrecord as vr, vcourse_video as vv , vcourse_course as vc , vcourse_technology as vt where vt.id=vc.tech_id and vr.user_id=%s and vr.video_id=vv.id and vr.course_id=vc.id GROUP BY id" % user.id
        courses_learning = dictfetchall(sql)
        task_create = task_daily(user)
        if task_create:
            flag, tasks = task_finish(user)  # 判断是否完成今日任务, 并返回
        else:
            flag, tasks = False, []

        if user.pathid == 0 or not Path.objects.filter(id=user.pathid).exists():
            if not WatchRecord.objects.filter(user_id=user.id).exists():
                return HttpResponseRedirect('/course/tracks')

        # 显示正在学习的路线
        else:
            path = Path.objects.get(id=user.pathid)

            courses_objs, courses = path.get_after_sorted_course()

            # 获取用户观看过当前路线的课程,是否观看完成
            courses_wathced = WatchCourse.objects.filter(user=user, course__in=path.course.all())

            # 课程时间显示转换, 如果以看完课程,显示课程观看时间, 如果没有看完课程,显示课程总时间
            for item in courses:
                for course_wathced in courses_wathced:
                    if item["id"] == course_wathced.course_id:
                        item['viewtime'] = '%s%s' % (time_comp_now(course_wathced.createtime), '完成')
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
                    ret_video = Video.objects.filter(course=item["id"])
                    if not ret_video.exists():
                        # 如果添加了课程,但是没有为课程添加视频, 默认读取第一个视频
                        ret_sql_v = Video.objects.order_by("sequence").first()
                        item['video_id'] = ret_sql_v.id
                        item['vtype'] = ret_sql_v.vtype
                        item['createtime'] = 0
                        item['video_name'] = ret_sql_v.name
                    else:
                        item['video_id'] = ret_video.first().id
                        item['video_name'] = ret_video.first().name
                        item['vtype'] = ret_video.first().vtype
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
            jindu, jindu_2 = track_process(user.id, courses_objs)
            result_dict = {
                'courses_path': courses,
                'jindu': jindu,
                'path_name': path.name,
                'courses': courses_learning,
                'xingxing': [0, 1, 2, 3, 4],
                'path_flag': True,
                'tasks': tasks,
                'flag': flag,
                'userplan': userplan
            }

            # 统计各个技能点的学习进度，页面嵌套环形图使用
            statistics_dict = statistics_skill_mastery_level_by_path(user.id, user.pathid)
            result_dict.update(statistics_dict)

            return render(request, 'dashBoard.html',result_dict)

        return render(request, 'dashBoard.html',
                      {'courses': courses_learning, 'path_flag': False, 'xingxing': [0, 1, 2, 3, 4], 'flag': flag,
                       'tasks': tasks, 'userplan': userplan,
                       "skill_name_data": [],  # 路线下所有技能点
                       "undone_color_data": [],  # 技能点未完成底色
                       "inner_ring_data": [],  # 内环技能点占比
                       "outer_ring_data": [],  # 外环技能点完成占比
                       })
    except:
        logging.getLogger().error(traceback.format_exc())
        return render(request, '404.html')


def task_daily(user):
    """创建每日任务"""
    try:
        today = time.strftime('%Y-%m-%d')
        ret = WatchRecord.objects.filter(user=user).exists()
        d_ret = DailyTask.objects.filter(createtime=today, user_id=user.id).exists()
        user_plan = Userplan.objects.filter(userid=user.id, createtime=today).values().first()
        if ret and not d_ret:
            sql = 'select vw.*, vv.sequence from vrecord_watchrecord as vw, vcourse_video as vv where user_id = %s and vw.video_id=vv.id order by createtime desc limit 1;' % user.id
            result = dictfetchall(sql)
            if user_plan:
                seqs = [str(result[0]['sequence'] + i) for i in range(1, user_plan['nums'])]
            else:
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
        else:
            return True
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


        #11111
        user = user_obj
        today = time.strftime('%Y-%m-%d')
        userplan = Userplan.objects.filter(userid=user_obj.id, createtime=today).values().first()
        # 显示已经学过的或者正在学习的课程
        sql = "select vr.video_id, vv.vtype as video_type, vc.*, vt.color as tech_color, vt.name as tech_name from vrecord_watchrecord as vr, vcourse_video as vv , vcourse_course as vc , vcourse_technology as vt where vt.id=vc.tech_id and vr.user_id=%s and vr.video_id=vv.id and vr.course_id=vc.id GROUP BY id" % user.id
        courses_learning = dictfetchall(sql)
        task_create = task_daily(user)
        if task_create:
            flag, tasks = task_finish(user)  # 判断是否完成今日任务, 并返回
        else:
            flag, tasks = False, []
        aaa = dict()

        if user.pathid == 0 or not Path.objects.filter(id=user.pathid).exists():
            if not WatchRecord.objects.filter(user_id=user.id).exists():
                return HttpResponseRedirect('/course/tracks')

        # 显示正在学习的路线
        else:
            path = Path.objects.get(id=user.pathid)

            courses_objs, courses = path.get_after_sorted_course()

            # 获取用户观看过当前路线的课程,是否观看完成
            courses_wathced = WatchCourse.objects.filter(user=user, course__in=path.course.all())

            # 课程时间显示转换, 如果以看完课程,显示课程观看时间, 如果没有看完课程,显示课程总时间
            for item in courses:
                for course_wathced in courses_wathced:
                    if item["id"] == course_wathced.course_id:
                        item['viewtime'] = '%s%s' % (time_comp_now(course_wathced.createtime), '完成')
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
                    ret_video = Video.objects.filter(course=item["id"])
                    if not ret_video.exists():
                        # 如果添加了课程,但是没有为课程添加视频, 默认读取第一个视频
                        ret_sql_v = Video.objects.order_by("sequence").first()
                        item['video_id'] = ret_sql_v.id
                        item['vtype'] = ret_sql_v.vtype
                        item['createtime'] = 0
                        item['video_name'] = ret_sql_v.name
                    else:
                        item['video_id'] = ret_video.first().id
                        item['video_name'] = ret_video.first().name
                        item['vtype'] = ret_video.first().vtype
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
            jindu, jindu_2 = track_process(user.id, courses_objs)
            print courses_learning
            result_dict = {
                'courses_path': courses,
                'jindu': jindu,
                'path_name': path.name,
                'courses': courses_learning,
                'xingxing': [0, 1, 2, 3, 4],
                'path_flag': True,
                'tasks': tasks,
                'flag': flag,
                'userplan': userplan
            }

            # 统计各个技能点的学习进度，页面嵌套环形图使用
            statistics_dict = statistics_skill_mastery_level_by_path(user.id, user.pathid)
            result_dict.update(statistics_dict)

        #11111
        result_dicta= {'user': user_obj, 'tech_score': tech_score, 'badges': badges, 'badgesLen': len(badges),
                       'totaltime': sum_watch_video_time['totaltime']}
        result_dicta.update(result_dict)
        return render(request, 'personalCenter.html',result_dicta)
    except:
        logging.getLogger().error(traceback.format_exc())
        return render(request, '404.html')


@require_login()
def editpage(request):
    """个人编辑页面"""
    try:
        if request.method == 'GET':
            uid = request.session['user']['id']
            user = User.objects.get(id=uid)
            return render(request, 'personedit.html', {'user': user})
        else:
            return HttpResponse(u'请求错误')
    except:
        logging.getLogger().error(traceback.format_exc())
        return render(request, '404.html')


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


@require_login()
def change_headimg(request):
    """修改个人头像呢"""
    try:
        if request.method == 'POST':
            headimg = request.FILES.get('headimg', None)
            uid = request.POST.get('uid', None)
            head_img_type = request.POST.get('head_img_type', None)
            if not headimg:
                return HttpResponse('no headimg for upload!')
            destination = os.path.join(settings.MEDIA_ROOT, 'user_headimg')
            if head_img_type == "resume_user_headimg":
                destination = os.path.join(settings.MEDIA_ROOT, 'resume_user_headimg')
            # print head_img_type
            # print destination
            if not os.path.isdir(destination):
                os.system('mkdir -p %s ' % destination)
            user = User.objects.get(id=uid)
            filename = str(user.id) + '_' + time.strftime('%y%m%d') + '.jpg'
            logging.getLogger().error(filename)
            headfile = open(os.path.join(destination, filename), 'wb')
            for chunk in headimg.chunks():
                headfile.write(chunk)
            headfile.close()

            headimg_url = '/media/user_headimg/%s' % filename
            if head_img_type == "resume_user_headimg":
                resume_obj = Resume.objects.filter(user_id=user).first()
                headimg_url = '/media/resume_user_headimg/%s' % filename
                if resume_obj:
                    resume_obj.head_img = headimg_url
                    resume_obj.save()
                else:
                    Resume.objects.create(user_id=user, head_img=headimg_url)
                return HttpResponse(json.dumps({'headimg': headimg_url}))
            else:
                user.headimg = headimg_url
                user.save()
            return HttpResponse(json.dumps({'headimg': '/media/user_headimg/%s' % filename}))
        return HttpResponse('get method ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


@require_login()
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


@require_login()
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


@require_login()
def editelse(request):
    """用户编辑页面修改"""
    try:
        if request.method == 'POST':
            print request.POST
            userid = request.session['user']['id']
            birthday = request.POST.get('birthday')
            edution = request.POST.get('edution')
            collegename = request.POST.get('collegename')
            borncity = request.POST.get('borncity')
            realname = request.POST.get('realname')
            xingzuo = request.POST.get('xingzuo')
            blood = request.POST.get('blood')
            expect_job = request.POST.get('expect_job')
            expect_salary = request.POST.get('expect_salary')
            intro = request.POST.get('content')
            email = request.POST.get('email')
            print userid, birthday, expect_job
            User.objects.filter(id=userid).update(birthday=birthday, edution=edution, collegename=collegename,
                                                  borncity=borncity, realname=realname, xingzuo=xingzuo, blood=blood,
                                                  expect_job=expect_job, expect_salary=expect_salary, intro=intro, email=email)
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
                courses, courses_values = pobj.get_after_sorted_course()
                pathname = pobj.name
                user['track_process'] = track_process(user['id'], courses)[0]
                user['track_name'] = pathname
        return render(request, 'xueyuanliebiao.html', {'users': users})
    except:
        logging.getLogger().error(traceback.format_exc())
        return render(request, '404.html')


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
                courses, courses_valuse = pobj.get_after_sorted_course()
                pathname = pobj.name
                user['track_process'] = track_process(user['id'], courses)[0]
                user['track_name'] = pathname
            return render(request, 'uinfo.html', {'user': user})
        else:
            return page_not_found(request)
    except:
        logging.getLogger().error(traceback.format_exc())
        return render(request, '404.html')


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
            return HttpResponse(json.dumps({'code': 0}))
        else:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请使用post method'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return render(request, '404.html')


def studydetail(request):
    return render(request, 'xuexixiangqing.html')


def collect(request):
    """收集信息"""
    try:
        if request.method == "POST":
            data = request.POST

            logging.getLogger().error(data)
            logging.getLogger().error(data['a'])
            return HttpResponse('ok')
    except:
            return HttpResponse('not ok')

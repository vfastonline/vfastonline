# encoding: utf-8
from models import Inform, InformTask, Feedback
from vuser.models import User
from django.http import HttpResponse, HttpResponseRedirect
from vfast.api import time_comp_now, require_login, dictfetchall
from vrecord.api import  track_skill

import traceback
import json
import logging
import time
from datetime import date


def test(request):
    print 'info test~!'

    user = User.objects.get(id=request.session['user']['id'])
    track_skill(user)
    return HttpResponse('ok')

# Create your views here.
def create_info_user(request):
    """生成用户通知"""
    try:
        today = date.today()
        today_inform = InformTask.objects.filter(pubtime__gt=today)
        uids = User.objects.filter().values('id')
        # print uids, today_inform
        for inform in today_inform:
            informtask = InformTask.objects.get(id=inform.id)
            for uid in uids:
                user = User.objects.get(id=uid['id'])
                if informtask.status == 0:
                    Inform.objects.create(user=user, desc=inform.desc, type=informtask.type, pubtime=informtask.pubtime,
                                          url=informtask.url, color=informtask.color)
                else:
                    logging.getLogger().warning('informtask repetition warning')
                    pass
            # 跑完的任务由状态0改为状态1
            informtask.status = 1
            informtask.save()
        return HttpResponse(json.dumps({'code': 0, 'msg': 'successfully'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def getinfo(request):
    """用户获取通知"""
    try:
        if request.method == 'GET':
            try:
                uid = request.session['user']['id']
            except KeyError:
                return HttpResponseRedirect('/login')
            user = User.objects.get(id=uid)
            informs = Inform.objects.filter(user=user).values('color', 'pubtime', 'desc',
                                                              'type__name', 'type_id', 'url', 'id')
            informations = []
            # print informs
            for item in informs:
                # print item
                tmp = dict(color=item['color'], desc=item['desc'], type=item['type_id'],
                           pubtime=time_comp_now(item['pubtime'].strftime('%Y-%m-%d %H:%M:%S')),
                           type_name=item['type__name'],
                           url=item['url'], inform_id=item['id'])
                informations.append(tmp)
            return HttpResponse(json.dumps(informations, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def del_all_info_user(request):
    """删除用户所有的通知"""
    try:
        if request.method == 'GET':
            try:
                uid = request.session['user']['id']
            except KeyError:
                return HttpResponseRedirect('/login')
            user = User.objects.get(id=uid)
            Inform.objects.filter(user=user).delete()
            return HttpResponse(json.dumps({'code': 0, 'msg': 'delete all inform successfully'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


def del_info_user(request):
    """删除用户指定的通知"""
    try:
        if request.method == "GET":
            try:
                uid = request.session['user']['id']
            except KeyError:
                return HttpResponseRedirect('/login')
            user = User.objects.get(id=uid)
            inform_id = request.GET.get('inform_id')
            Inform.objects.filter(user=user, id=inform_id).delete()
            return HttpResponse(json.dumps({'code': 0, 'msg': 'delete inform successfully'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))


@require_login()
def create_feedback(request):
    """接受用户反馈"""
    try:
        if request.method == "POST":
            try:
                uid = request.session['user']['id']
                user = User.objects.get(id=uid)
                description = request.POST.get('description')
                userip = request.META.get('REMOTE_ADDR')
                http_user_agent = request.META.get('HTTP_USER_AGENT')
                create_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print create_time, http_user_agent, description
                Feedback.objects.create(user=user, description=description, userip=userip, createtime=create_time,
                                        user_agent=http_user_agent)
                return HttpResponse(json.dumps({'code':0}))
            except:
                logging.getLogger().error(traceback.format_exc())
                return HttpResponse(json.dumps({'code':1}))
        else:
            return HttpResponse(json.dumps({'code':2}))
    except:
        return HttpResponse(json.dumps({'code':3}))


def daily_mail(request):
    try:
        # yesterday = time.strftime('%Y-%m-%d',time.localtime(time.time() - 24*60*60))
        yesterday = '2017-07-25'
        sql = "select pathid, id as user_id from vuser_user where id in (select user_id from vrecord_score where createtime = '%s' group by user_id);" % yesterday
        sql_result = dictfetchall(sql)
        for value in sql_result:
            user = User.objects.get(id=value['user_id'])
            #用户邮箱不为空, 且正在进行一个学习路线,发送每日邮件
            if value['pathid'] != 0 and user.email:
                sql_path = 'select name from vcourse_path where id = %s' % value['pathid']
                pathname = dictfetchall(sql_path)
                sql_course = "select vw.createtime, vc.name, vc.id  from vrecord_watchrecord as vw left join  vcourse_course as vc on vw.course_id = vc.id where vw.user_id = %s order by createtime desc limit 1" % value['user_id']
                sql_course_result = dictfetchall(sql_course)
                # print sql_course_result
                path = dict(id=value['pathid'], name = pathname[0]['name'])
                course = dict(id=sql_course_result[0]['id'], name=sql_course_result[0]['name'])
                grain_skill, skill = track_skill(user)

                rank_sql = "select vu.id, ifnull(vv.score,0) as score, vu.headimg, vu.nickname from vuser_user as vu left join (select user_id , sum(score) as score from vrecord_score group by user_id ) as vv on vu.id=vv.user_id order by score desc;"
                rank_result= dictfetchall(rank_sql)
                for user_pos in rank_result:
                    if user_pos['id'] == value['user_id']:
                        position = rank_result.index(user_pos)
                if position == 0:
                    rank = rank_result[:2]
                elif position == len(rank_result) - 1:
                    rank = rank_result[-2:]
                else:
                    rank = rank_result[position-1: position+2]
                for item in rank:
                    sql_yesterday = "select sum(score) as score from vrecord_score where user_id = %s and createtime='%s';" % (
                    item['id'], yesterday)
                    score_yesterday = dictfetchall(sql_yesterday)[0]['score']
                    item['score_yesterday'] = score_yesterday
                print rank                    #排行榜   三个
                print grain_skill, skill      #技能点
                print path, course,           #路线, 课程
                print user.nickname           #用户别名
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                # return rank, grain_skill,skill, path, course, user.nickname

        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')

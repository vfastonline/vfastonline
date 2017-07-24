# encoding: utf-8
from django.shortcuts import render
from models import Inform, InformTask, Feedback
from vuser.models import User
from django.http import HttpResponse, HttpResponseRedirect
from vfast.api import time_comp_now, require_login

import traceback
import json
import logging
import time
from datetime import date


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

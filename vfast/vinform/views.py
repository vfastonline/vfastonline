# encoding: utf-8
from django.shortcuts import render
from models import Inform, InformTask
from vuser.models import User
from django.http import HttpResponse, HttpResponseRedirect

import traceback
import json
import logging
import time


# Create your views here.
def create_info_user(request):
    """生成用户通知"""
    try:
        today = time.strftime('%Y-%m-%d')
        today_inform = InformTask.objects.filter(pubtime=today)
        uids = User.objects.filter().values('id')
        print uids, today_inform
        for uid in uids:
            user = User.objects.get(id=uid['id'])
            for inform in today_inform:
                informtask = InformTask.objects.get(id=inform.id)
                if informtask.status == 0:
                    Inform.objects.create(user=user, desc=inform.desc, type=informtask.type, pubtime=informtask.pubtime,
                                          url=informtask.url)
                    # 跑完的任务由状态0改为状态1
                    informtask.status = 1
                    informtask.save()
                else:
                    logging.getLogger().warning('informtask repetition warning')
        return HttpResponse(json.dumps({'code': 0, 'msg': 'successfully'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': 'failed'}, ensure_ascii=False))


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
                                                              'type__name', 'type_id', 'url')
            informations = []
            for item in informs:
                tmp = dict(color=item['color'], desc=item['desc'], type=item['type_id'],
                           pubtime=str(item['pubtime']), type_name=item['type__name'],
                           url=item['url'])
                informations.append(tmp)
            return HttpResponse(json.dumps(informations, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': 'failed'}, ensure_ascii=False))


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
        return HttpResponse(json.dumps({'code': 1, 'msg': 'delete all inform failed'}, ensure_ascii=False))


def del_info_user(request):
    """删除用户指定的通知"""
    try:
        if request.method == "GET":
            try:
                uid = request.session['user']['id']
            except KeyError:
                return HttpResponseRedirect('/login')
            user = User.objects.get(id=uid)
            inform_id = request.POST.get('inform_id')
            Inform.objects.filter(user=user, id=inform_id).delete()
            return HttpResponse(json.dumps({'code': 0, 'msg': 'delete inform successfully'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': 'delete all inform failed'}, ensure_ascii=False))

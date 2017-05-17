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
        today_infor = InformTask.objects.filter(pubtime=today)
        uids = User.objects.filter().values('id')
        print uids, today_infor
        for uid in uids:
            for infor in today_infor:
                user = User.objects.get(id=uid['id'])
                infor = InformTask.objects.get(id=infor.id)
                Inform.objects.create(user=user, infor=infor)
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
            informs = Inform.objects.filter(user=user).values('infor__color', 'infor__pubtime', 'infor__type',
                                                              'infor__desc', 'infor__type__name', 'infor__url')
            informations = []
            for item in informs:
                tmp = dict(color=item['infor__color'], desc=item['infor__desc'], type=item['infor__type'],
                           pubtime=str(item['infor__pubtime']), type_name=item['infor__type__name'], url=item['infor__url'])
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
            return HttpResponse(json.dumps({'code':0, 'msg':'delete all inform successfully'}))
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
            inform = InformTask.objects.get(id=inform_id)
            Inform.objects.filter(user=user, infor=inform).delete()
            return HttpResponse(json.dumps({'code':0, 'msg':'delete inform successfully'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': 'delete all inform failed'}, ensure_ascii=False))


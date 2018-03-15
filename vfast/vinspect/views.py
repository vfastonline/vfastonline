#!/usr/bin/env python
#encoding:utf-8
from django.shortcuts import render
from vinspect.models import Inspect, InspectOption, InspectResult
from django.http import HttpResponse
from vfast.api import require_login, Handleformdata
from vuser.models import User

import logging
import traceback
import json
# Create your views here.



def inspect_list(request):
    """问卷调查列表页"""
    try:
        inspects = Inspect.objects.all()
        print inspects

        return render(request, 'inspectlist.html', {'inspects':inspects})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def inspect_detail(request, inspectid):
    """问卷调查详细页面"""
    try:
        try:
            inspectid = int(inspectid)
        except ValueError:
            return HttpResponse(json.dumps({'code':1, 'msg':'unvalid parameters'}))
        if isinstance(inspectid, int):
            inspectid = inspectid
            obj = Inspect.objects.get(id=inspectid)
            options = InspectOption.objects.filter(inspect=obj).values()
            return render(request, 'inspectdetail.html', {'options':options, 'inspect':obj})
        else:
            return HttpResponse(status=403)
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':128, 'msg':'web server 500'}))


@require_login()
def inspect_result(request):
    """问卷调查收集"""
    try:
        if request.method == "POST":
            userid = request.session['user']['id']
            user = User.objects.get(id=userid)
            data = request.POST.get('data')
            data = Handleformdata(data)

            inspectid = data['inspectid']
            opinion = data['opinion']

            data.pop('opinion')
            data.pop('inspectid')
            inspect = Inspect.objects.get(id=inspectid)
            if  InspectResult.objects.filter(user=user, inspect=inspect, opinion__isnull=False).exists():
                return HttpResponse(json.dumps({'code': 1, 'msg':'你之前已经评论过~!'},ensure_ascii=False))
            for k, v in data.iteritems():
                inspectoption = InspectOption.objects.get(id=int(k))
                InspectResult.objects.create(user=user, inspect=inspect, option=v, inspectoption=inspectoption)

            InspectResult.objects.create(user=user, inspect=inspect, opinion=opinion)

            return HttpResponse(json.dumps({'code':0, 'msg':'感谢您的参与,评论成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code':1, 'msg':'请使用POST方法!'}, ensure_ascii=False))

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':128, 'msg':'服务器错误'},ensure_ascii=False))





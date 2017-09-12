#!/usr/bin/env python
#encoding:utf-8
from django.shortcuts import render
from vinspect.models import Inspect, InspectOption, InspectResult
from django.http import HttpResponse
from vfast.api import require_login
from vuser.models import User

import logging
import traceback
import json
# Create your views here.



def inspect_list(request):
    """问卷调查列表页"""
    try:
        pass
    except:
        pass


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


# @require_login()
def inspect_result(request):
    """问卷调查收集"""
    try:
        user = User.objects.get(id=2)
        if request.method == "POST":
            data = request.POST.get('data')
            data = json.loads(data)
            # print data
            options = data.get('options')
            opinion = data.get('opinion')
            inspectid = data.get('inspectid')

            inspect = Inspect.objects.get(id=inspectid)
            # print inspect.name
            for item in options:
                inspectoption = InspectOption.objects.get(id=item['optionid'])
                InspectResult.objects.create(user=user, inspect=inspect, option=item['option'],inspectoption=inspectoption)

            InspectResult.objects.create(user=user, inspect=inspect, opinion=opinion)

            return HttpResponse(json.dumps({'code':0}))
        else:
            return HttpResponse({'code':1})

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':128}))





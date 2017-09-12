#!/usr/bin/env python
#encoding:utf-8
from django.shortcuts import render
from vinspect.models import Inspect, InspectOption, InspectResult
from django.http import HttpResponse

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


def inspect_result(request):
    """问卷调查收集"""
    try:
        pass
    except:
        pass





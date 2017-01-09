#!encoding:utf-8
import logging, traceback
import json

from vcourse.models import TypeFunc, TypeProgram
from vfast.api import get_object
from django.shortcuts import render
from django.http import HttpResponse
from vfast.api import get_object

# Create your views here.
def test(request):
    return HttpResponse('hello,world~!')

def course_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'coursetest.html')
        else:
            name = request.POST.get('name')
            desc = request.POST.get('desc', ' ')
            totaltime = request.POST.get('totaltime', ' ')
            difficult = request.POST.get('difficult', ' ')
            color = request.POST.get('color', ' ')
            pubstatus = request.POST.get('pubstatus', ' ')
            subscibe = request.POST.get('subscibe', ' ')
            cl_id = request.POST.get('cl_id', None)
            # if cl_id:

    except:
        logging.getLogger().error(traceback)
        return HttpResponse(json.dumps({'code':1, 'msg': u'服务器错误'}, ensure_ascii=False))

def video_add(request):
    pass


def path_add(request):
    pass


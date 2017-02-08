#!encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from vgrade.models import Headframe, Headimg

import os
import time
import logging
import traceback

# Create your views here.
def test(request):
    return HttpResponse('badge test')

#用户头像边框上传
def headframe_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'du/hframe.html')
        else:
            name = request.POST.get('name')
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            hffile = request.FILES.get('headframe', None)
            url = '/static/head/' + hffile.name if hffile else ' '
            mpath = os.path.join(settings.IMG_ROOT, 'static/head')
            os.system('mkdir -p %s' % mpath)
            print mpath
            try:
                filename = open(os.path.join(mpath, hffile.name), 'wb+')
                for chunk in hffile.chunks():
                    filename.write(chunk)
                filename.close()
            except AttributeError:
                logging.getLogger().error(u'保存上传边框图片时错误')

            Headframe.objects.create(name=name, createtime = t, url=url)
        return HttpResponse('head ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


#用户头像上传
def headimg_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'du/hframe.html')
        else:
            name = request.POST.get('name')
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            headfile = request.FILES.get('headimg', None)
            url = '/static/head/' + headfile.name if headfile else ' '
            mpath = os.path.join(settings.IMG_ROOT, 'static/head')
            os.system('mkdir -p %s' % mpath)
            print mpath
            try:
                filename = open(os.path.join(mpath, headfile.name), 'wb+')
                for chunk in headfile.chunks():
                    filename.write(chunk)
                filename.close()
            except AttributeError:
                logging.getLogger().error(u'保存上传头像图片时错误')

            Headimg.objects.create(name=name, createtime = t, url=url, type=1)
        return HttpResponse('head ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')
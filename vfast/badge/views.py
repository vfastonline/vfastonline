#!encoding: utf-8
from vfast.api import get_object
from vcourse.models import Course
from badge.models import Badge
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import logging, traceback
import os, time , json
# Create your views here.

def badge_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'badgetest.html')
        else:
            badgename = request.POST.get('badgename')
            badgeimg = request.FILES['badgeimg']
            cid = request.POST.get('cid')
            cid_object = get_object(Course, id=cid)
            createtime = int(time.time())
            fs = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'img'))
            filename = fs.save(badgeimg.name, badgeimg)
            uploaded_file_url = '/img'+fs.url(filename)
            print badgename, cid_object.name, filename, uploaded_file_url, createtime
            Badge.objects.get_or_create(badgename=badgename, cid=cid_object, createtime=createtime, badgeurl=uploaded_file_url)
            return HttpResponse(json.dumps({'code':0 ,'msg': u'创建勋章成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1 , 'msg': u'创建勋章失败'}, ensure_ascii=False))


def badge_get(request):
    try:
        id = request.GET.get('id', None)
        print id
        if id:
            badge = Badge.objects.get(id=id)
            print badge
            return HttpResponse('id ok')
        else:
            badgename = request.GET.get('name')
            badge = Badge.objects.filter(badgename=badgename).first()
            print badge
            return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')



def badge_edit(request):
    try:
        if request.method == 'GET':
            return render(request, 'badgetest.html')
        else:
            pass
    except:
        logging.getLogger().error(traceback)
        return HttpResponse(json.dumps({'code':1, 'msg': '服务器错误'}, ensure_ascii=False))


def badge_del(request):
    pass


def badge_getall(request):
    pass


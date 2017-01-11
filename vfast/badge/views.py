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
    """添加勋章"""
    try:
        if request.method == 'GET':
            return render(request, 'badgetest.html')
        else:
            badgename = request.POST.get('badgename')
            badgeimg = request.FILES['badgeimg']
            cid = request.POST.get('cid')
            course = get_object(Course, id=cid)
            createtime = time.strftime('%Y-%m-%d %H:%M:%D')

            uploaded_file_url = 'img/' + badgeimg.name
            dest = open(os.path.join(settings.MEDIA_ROOT, uploaded_file_url), 'wb+')
            for chunk in badgeimg.chunks():
                dest.write(chunk)
            dest.close()

            print badgename, course.name, uploaded_file_url, createtime
            Badge.objects.get_or_create(badgename=badgename, course=course, createtime=createtime, badgeurl=uploaded_file_url)
            return HttpResponse(json.dumps({'code':0 ,'msg': u'创建勋章成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1 , 'msg': u'创建勋章失败'}, ensure_ascii=False))


def badge_get(request):
    """获取勋章"""
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
    """编辑勋章"""
    try:
        if request.method == 'GET':
            id = request.GET.get('id')
            badge = Badge.objects.get(id=id)
            return render(request, 'badgetest.html')
        else:
            id = request.POST.get('id', '')
            badgename = request.POST.get('badgename')
            cid = request.POST.get('cid', None)
            course = Course.objects.get(id=cid)
            Badge.objects.filter(id=id).update(course=course, badgename=badgename)
            return HttpResponse(json.dumps({'code':0, 'msg': u'修改勋章信息成功'}))
    except:
        logging.getLogger().error(traceback)
        return HttpResponse(json.dumps({'code':1, 'msg': '服务器错误'}, ensure_ascii=False))


def badge_del(request):
    """删除勋章"""
    try:
        if request.method == "GET":
            id = request.GET.get('id')
        else:
            id = request.POST.get('id')
        Badge.objects.get(id=id).delete()
        return HttpResponse(json.dumps({'code':0, 'msg': u'删除成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': u'服务器错误'}, ensure_ascii=False))


def badge_getall(request):
    """获取所有勋章"""
    try:
        badges = Badge.objects.filter().all()
        print badges
        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1, 'msg': u'服务器错误'}, ensure_ascii=False))


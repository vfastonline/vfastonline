#!encoding:utf-8
from vcourse.models import Course
from django.shortcuts import render
from django.db import connection
from vgrade.api import headimg_urls
import random
from vcourse.models import Program
from vfast.api import get_id_name, require_role, require_login
from vrecord.views import course_watched_all
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from vuser.models import User
from django.db.models import F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from vcourse.models import Video

import logging
import traceback
import json



# @require_login()
# @require_role(role=1)
def test(request):
    print 'test'
    # course = connection.cursor()
    # course.execute('select * from vcourse_video')
    # a = dictfetchall(cursor=course)
    return HttpResponse('test')

def dashBoard(request):
    return render(request, 'DashBoard.html')

def learning_path(request):
    return render(request, 'learning_path.html')

def course_library(request):
    return render(request, 'course_library.html')


def logout(request):
    # print 'del session'
    # del request.session['token']
    del request.session['login']
    del request.session['user']
    return HttpResponse('del session ok')


# @require_login()
def index(request):
    return render(request, 'index.html')


def search(request):
    try:
        key_words =request.GET.get('query')
        print key_words
        results = Course.objects.filter(name__contains=key_words).values()
        print results
        return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def search_js(request):
    try:
        course_names = Course.objects.all().values('name')
        cnames = [item['name'] for item in course_names]
        return HttpResponse(json.dumps({'name': cnames}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')



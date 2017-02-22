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

import logging
import traceback
import json


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# @require_login()
# @require_role(role=1)
def test(request):
    print 'test'
    course = connection.cursor()
    course.execute('select * from vuser_user')
    a = dictfetchall(cursor=course)
    return HttpResponse(json.dumps({'result': a},ensure_ascii=False))
    return HttpResponse('test')

def dashBoard(request):
    return render(request, 'DashBoard.html')


def logout(request):
    # print 'del session'
    # del request.session['token']
    del request.session['login']
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



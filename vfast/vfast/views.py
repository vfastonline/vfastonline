#!encoding:utf-8
from django.shortcuts import render
from django.db import connection
from vgrade.api import headimg_urls
import random
from vcourse.models import Program
from vfast.api import get_id_name, require_role, require_login
from vrecord.views import course_watched_all
from django.core.urlresolvers import reverse
from django.http import HttpResponse

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@require_login()
# @require_role(role=1)
def test(request):
    print 'test'
    # print request.session.get('token', 'bucunzai')
    # user = request.session.get('user')
    return render(request, 'du/testdu.html')

def logout(request):
    print 'del session'
    del request.session['token']
    return HttpResponse('del session ok')

def index(request):
    return render(request, 'index.html')


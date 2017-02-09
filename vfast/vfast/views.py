#!encoding:utf-8
from django.shortcuts import render
from django.db import connection
from vgrade.api import headimg_urls
import random
from vcourse.models import Program
from vfast.api import get_id_name
from vrecord.views import course_watched_all

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def test(request):
    print 'test'
    print course_watched_all(1,2)
    return render(request, 'du/testdu.html')


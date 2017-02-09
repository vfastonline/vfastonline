#!encoding:utf-8
from django.shortcuts import render
from vgrade.api import headimg_urls
import random
from vcourse.models import Program
from vfast.api import get_id_name

def test(request):
    print 'test'
    print headimg_urls()
    # print random.choice(headimg_urls().values())
    # print Program.objects.all()
    # print get_id_name(Program)
    return render(request, 'du/testdu.html')


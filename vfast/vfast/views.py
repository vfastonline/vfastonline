#!encoding:utf-8
from django.shortcuts import render
from vgrade.api import headimg_urls
import random
from vcourse.models import Program
def test(request):
    print 'test'
    print random.choice(headimg_urls().values())
    print Program.objects.all()
    return render(request, 'du/testdu.html')


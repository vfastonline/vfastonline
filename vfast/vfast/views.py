#!encoding:utf-8
from django.shortcuts import render
from vgrade.api import headimg_urls
import random

def test(request):
    print 'test'
    print random.choice(headimg_urls().values())
    return render(request, 'du/testdu.html')


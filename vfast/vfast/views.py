#!encoding:utf-8
from django.shortcuts import render

def test(request):
    print 'test'
    return render(request, 'test.html')
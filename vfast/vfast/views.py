#!encoding:utf-8
from django.shortcuts import render
from record.recordapi import get_score, get_watchtime
from record.models import WatchRecord, Score

def test(request):
    print 'test'
    # print get_score(Score, uid=1)
    # print get_score(Score)
    # print get_watchtime(WatchRecord, uid=1)
    # print get_watchtime(WatchRecord, uid=4)
    print get_watchtime(WatchRecord)
    return render(request, 'testdu.html')


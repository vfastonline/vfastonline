#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from vuser.models import User
from vcourse.models import Video
from vpractice.models import Question

import logging
import traceback
import time

# Create your views here.
def add_question(request):
    try:
        try:
            userid = request.session['user']['id']
            user = User.objects.get(id=userid)
        except:
            return HttpResponse('用户未登录')
        title = request.GET.get('title')
        desc = request.GET.get('desc')
        createtime = time.strftime('%Y-%m-%d %H:%M:%S')
        vid = request.GET.get('vid')
        video = Video.objects.get(id=vid)
        email_status = request.GET.get('email')
        try:
            Question.objects.create(title=title, desc=desc, user=user, video=video, createtime=createtime, email_status=email_status)
            return HttpResponse('ok')
        except:
            return HttpResponse('database error')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


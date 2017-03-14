#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from vuser.models import User
from vcourse.models import Video
from vpractice.models import Question

import logging
import traceback
import time
import json


# Create your views here.
def add_question(request):
    try:
        if request.method == 'GET':
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
            print title, desc, video.name, email_status
            try:
                Question.objects.create(title=title, desc=desc, user=user, video=video, createtime=createtime,
                                        email_status=email_status, like=0)
                return HttpResponse(json.dumps({'code': 0}, ensure_ascii=False))
            except:
                logging.getLogger().error(traceback.format_exc())
                return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def question_list(request):
    try:
        pass
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def add_replay(request):
    try:
        try:
            userid = request.session['user']['id']
            user = User.objects.get(id=userid)
        except:
            return HttpResponse('用户未登录')
        content = request.GET.get('content')
        qid = request.GET.get('qid')
        question = Question.objects.get(id=qid)
        Question.objects.create(content=content, question=question, replay_user=user, like=0,
                                createtime=time.strftime('%Y-%m-%d %H:%M:%S'))
        return HttpResponse(json.dumps({'code': 0}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))

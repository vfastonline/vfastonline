#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from vuser.models import User
from vcourse.models import Video
from vpractice.models import Question, QuestionComment, ReplayComment, Replay, Attention

import logging
import traceback
import time
import json


# Create your views here.
def add_question(request):
    try:
        if request.method == 'POST':
            try:
                userid = request.session['user']['id']
                user = User.objects.get(id=userid)
            except:
                return HttpResponse('用户未登录')
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            print desc
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            vid = request.POST.get('vid')
            video = Video.objects.get(id=vid)
            email_status = request.POST.get('email')
            print title, desc, video.name, email_status
            try:
                ques = Question.objects.create(title=title, desc=desc, user=user, video=video, createtime=createtime,
                                               email_status=email_status, like=0)
                return HttpResponse(json.dumps({'code': 0, 'qid': ques.id}, ensure_ascii=False))
            except:
                logging.getLogger().error(traceback.format_exc())
                return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def question_comment(request):
    '''问题点赞功能'''
    try:
        qid = request.GET.get('qid')
        uid = request.GET.get('uid')
        type = request.GET.get('type')
        try:
            user_id = request.session['user']['id']
            if uid != user_id:
                return False
        except:
            return False
        ret = QuestionComment.objects.filter(qid=qid, uid=uid).exists()
        if ret:
            return HttpResponse(json.dumps({'code':0, 'msg': '你已经评论过'}))
        question = Question.objects.get(id=qid)
        if type == 'like':
            question.like += 1
        else:
            question.dislike += 1
        question.save()
        QuestionComment.objects.create(qid=qid, uid=uid)
        return HttpResponse(json.dumps({'code':0, 'msg': '评论成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def replay_comment(request):
    '''回复点赞功能'''
    try:
        qid = request.GET.get('qid')
        uid = request.GET.get('uid')
        type = request.GET.get('type')
        try:
            user_id = request.session['user']['id']
            if uid != user_id:
                return False
        except:
            return False
        ret = ReplayComment.objects.filter(qid=qid, uid=uid).exists()
        if ret:
            return HttpResponse(json.dumps({'code':0, 'msg': '你已经评论过'}))
        replay = Replay.objects.get(id=qid)
        if type == 'like':
            replay.like += 1
        else:
            replay.dislike += 1
        replay.save()
        QuestionComment.objects.create(qid=qid, uid=uid)
        return HttpResponse(json.dumps({'code':0, 'msg': '评论成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def attention_question(request):
    """关注问题功能"""
    try:
        qid = request.GET.get('qid')
        uid = request.GET.get('uid')
        try:
            user_id = request.session['user']['id']
            if uid != user_id:
                return False
        except:
            return False
        ret = Attention.objects.filter(qid=qid, uid=uid).exists()
        if ret:
            return HttpResponse(json.dumps({'code':0, 'msg': '你已经关注了此问题'}))
        Attention.objects.create(qid=qid, uid=uid)
        return HttpResponse(json.dumps({'code':0, 'msg': '关注成功'}))
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


def show_question(request):
    try:
        qid = request.GET.get('qid')
        print qid
        question = Question.objects.get(id=qid)
        print question.video.course.tech.name

        return render(request, 'detailsQA.html', {'question': question})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')




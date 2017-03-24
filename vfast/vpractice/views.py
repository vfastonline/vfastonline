#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from vuser.models import User
from vcourse.models import Video
from vpractice.models import Question, QRcomment, Replay, Attention
from django.db.models import Q

import logging
import traceback
import time
import json


# Create your views here.
def add_question(request):
    """添加问题"""
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
                                               email_status=email_status, like=0, dislike=0)
                return HttpResponse(json.dumps({'code': 0, 'qid': ques.id}, ensure_ascii=False))
            except:
                logging.getLogger().error(traceback.format_exc())
                return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def show_question(request):
    """查看问题"""
    try:
        try:
            uid = request.session['user']['id']
        except:
            return render(request, 'detailsQA.html')
        qid = request.GET.get('qid')
        question = Question.objects.get(id=qid)
        replays = Replay.objects.filter(question=question).values()
        attention = Attention.objects.filter(qid=qid, uid=uid).exists()
        qrcomment = QRcomment.objects.filter(uid=uid).values()

        qcomment = {}
        for qr in qrcomment:
            if qr['qid'] == question.id and qr['type'] == "Q" and qr['status'] == 1:
                qcomment['status'] = 'like'
            elif qr['qid'] == question.id and qr['type'] == "Q" and qr['status'] == 0:
                qcomment['status'] = 'dislike'
            else:
                qcomment = None
            for replay in replays:
                if qr['rid'] == replay['id'] and qr['type'] == "R" and qr['status'] == 1:
                    replay['status'] = 'like'
                elif qr['qid'] == replay['id'] and qr['type'] == "R" and qr['status'] == 0:
                    replay['status'] = 'dislike'
                else:
                    replay['status'] = None

        print attention, qcomment
        return render(request, 'detailsQA.html', {'question': question, 'replays': replays})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def add_replay(request):
    """添加回复"""
    try:
        try:
            userid = request.session['user']['id']
            user = User.objects.get(id=userid)
        except:
            return HttpResponse('用户未登录')
        content = request.GET.get('content')
        qid = request.GET.get('qid')
        question = Question.objects.get(id=qid)
        Question.objects.create(content=content, question=question, replay_user=user, like=0, dislike=0,
                                createtime=time.strftime('%Y-%m-%d %H:%M:%S'))
        return HttpResponse(json.dumps({'code': 0}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def qr_comment(request):
    '''问题回复点赞功能'''
    try:
        qid = request.GET.get('qid')
        rid = request.GET.get('rid')
        status = request.GET.get('status')
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请先登录'}))
        if QRcomment.objects.filter(qid=qid, uid=uid).exists():
            return HttpResponse(json.dumps({'code': 0, 'msg': '问题已经评论过'}))
        elif not QRcomment.objects.filter(qid=qid, uid=uid).exists() and qid:
            QRcomment.objects.create(qid=qid, uid=uid, type='Q', status=status)
        elif QRcomment.objects.filter(rid=rid, uid=uid).exists():
            return HttpResponse(json.dumps({'code': 0, 'msg': '回复你已经评论过'}))
        else:
            QRcomment.objects.create(qid=qid, uid=uid, type='R', status=status)
        return HttpResponse(json.dumps({'code': 0, 'msg': '评论成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


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
            return HttpResponse(json.dumps({'code': 0, 'msg': '你已经关注了此问题'}))
        Attention.objects.create(qid=qid, uid=uid)
        return HttpResponse(json.dumps({'code': 0, 'msg': '关注成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def question_list(request):
    """问题详情列表"""
    try:
        pass
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))

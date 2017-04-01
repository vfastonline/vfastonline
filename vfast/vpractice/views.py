#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from vuser.models import User
from vcourse.models import Video
from vpractice.models import Question, QRcomment, Replay, Attention
from django.db.models import Q, F

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
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            vid = request.POST.get('vid')
            video = Video.objects.get(id=vid)
            email_status = request.POST.get('email')
            # print title, desc, video.name, email_status
            try:
                ques = Question.objects.create(title=title, desc=desc, user=user, video=video, createtime=createtime,
                                               email_status=email_status, like=0, dislike=0, status=0)
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
        replays = Replay.objects.filter(question=question).values().order_by('-createtime')
        attention = Attention.objects.filter(qid=qid, uid=uid).exists()  # 用户是否关注问题
        qrcomment = QRcomment.objects.filter(uid=uid).values()

        qcomment = {}
        for item in replays:
            item['robj'] = Replay.objects.get(id=item['id'])
        for qr in qrcomment:
            if qr['qid'] == question.id and qr['type'] == "Q" and qr['status'] == 1:
                qcomment['status'] = 'like'
            elif qr['qid'] == question.id and qr['type'] == "Q" and qr['status'] == -1:
                qcomment['status'] = 'dislike'
            else:
                pass
            try:
                qcomment['status']
            except KeyError:
                qcomment['status'] = False

            for replay in replays:
                if qr['rid'] == replay['id'] and qr['type'] == "R" and qr['status'] == 1:
                    replay['status'] = 'like'
                elif qr['rid'] == replay['id'] and qr['type'] == "R" and qr['status'] == -1:
                    replay['status'] = 'dislike'
                else:
                    pass
        print replays
        # print attention, qcomment, replays
        # qcomment 用户是否对问题点赞, question 问题对象, relays 回复, attention 是否关注问题
        return render(request, 'detailsQA.html',
                      {'question': question, 'replays': replays, 'qcomment': qcomment, 'attention': attention})
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
        content = request.POST.get('content')
        qid = request.POST.get('qid')
        question = Question.objects.get(id=qid)
        # print question.user.username
        ret = Replay.objects.create(content=content, question=question, replay_user=user, like=0, dislike=0,
                                    createtime=time.strftime('%Y-%m-%d %H:%M:%S'), best=0)
        return HttpResponse(json.dumps({'code': 0, 'rid': ret.id}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def qr_comment(request):
    '''问题回复点赞功能'''
    try:
        qid = request.GET.get('qid')
        rid = request.GET.get('rid')
        status = request.GET.get('type')  # 1为赞, -1踩
        status = int(status)
        print status
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请先登录'}))
        if qid and QRcomment.objects.filter(qid=qid, uid=uid).exists():
            return HttpResponse(json.dumps({'code': 0, 'msg': '问题已经评论过'}))
        elif qid and QRcomment.objects.filter(qid=qid, uid=uid, type='Q').exists() == False:
            QRcomment.objects.create(qid=qid, uid=uid, type='Q', status=status)
            if status == 1:
                Question.objects.filter(id=qid).update(score=F('score') + status, like=F('like') + 1)
            else:
                Question.objects.filter(id=qid).update(score=F('score') + status, dislike=F('dislike') + 1)
        elif rid and QRcomment.objects.filter(rid=rid, uid=uid, type='R').exists() == False:
            QRcomment.objects.create(rid=rid, uid=uid, type='R', status=status)
            if status == 1:
                Replay.objects.filter(id=rid).update(score=F('score') + status, like=F('like') + 1)
            else:
                Replay.objects.filter(id=rid).update(score=F('score') + status, dislike=F('dislike') + 1)
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': '回复你已经评论过'}))
        return HttpResponse(json.dumps({'code': 0, 'msg': '评论成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def update_comment(request):
    '''修改问题回复点赞'''
    try:
        qid = request.GET.get('qid')
        rid = request.GET.get('rid')
        status = request.GET.get('type')  # 1为赞, -1踩
        status = int(status)
        print status
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请先登录'}))
        if qid and QRcomment.objects.filter(qid=qid, uid=uid, type='Q').exists():
            QRcomment.objects.filter(qid=qid, uid=uid, type='Q').update(status=status)
            if status == 1:
                Question.objects.filter(id=qid).update(score=F('score') + 2, like=F('like') + 1,
                                                       dislike=F('dislike') + 1)
            else:
                Question.objects.filter(id=qid).update(score=F('score') - 2, like=F('like') - 1,
                                                       dislike=F('dislike') + 1)
            return HttpResponse(u'修改问题评论成功')
        elif rid and QRcomment.objects.filter(rid=rid, uid=uid, type='R').exists():
            QRcomment.objects.filter(rid=rid, uid=uid, type='R').update(status=status)
            if status == 1:
                Replay.objects.filter(id=rid).update(score=F('score') + 2, like=F('like') + 1, dislike=F('dislike') + 1)
            else:
                Replay.objects.filter(id=rid).update(score=F('score') - 2, like=F('like') - 1, dislike=F('dislike') + 1)
            return HttpResponse(u'修改回复瓶成功')
        else:
            return HttpResponse('ok')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def attention_question(request):
    """关注问题功能"""
    try:
        qid = request.GET.get('qid')
        attention = request.GET.get('attention')  # 1关注问题, 0取消关注
        try:
            uid = request.session['user']['id']
        except:
            return False
        ret = Attention.objects.filter(qid=qid, uid=uid).exists()
        if ret and attention == '0':
            Attention.objects.filter(qid=qid, uid=uid).delete()
            return HttpResponse(json.dumps({'code': 0, 'msg': '取消关注成功'}))
        elif ret == False and attention == '1':
            Attention.objects.create(qid=qid, uid=uid)
            return HttpResponse(json.dumps({'code': 0, 'msg': '关注成功'}))
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'attention_question , interface right'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def question_detail(request):
    try:
        qid = request.GET.get('qid')
        question = Question.objects.filter(id=qid).values()[0]
        print question
        return HttpResponse(json.dumps({'question': question}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def replay_detail(request):
    try:
        rid = request.GET.get('rid')
        replay = Replay.objects.filter(id=rid).values()[0]
        print replay
        return HttpResponse(json.dumps({'replay': replay}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def update_question(request):
    try:
        qid = request.POST.get('qid')
        desc = request.POST.get('desc')
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        Question.objects.filter(id=qid).update(desc=desc, createtime=now)
        return HttpResponse(json.dumps({'code': 0, 'msg': u'编辑问题成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def update_replay(request):
    try:
        rid = request.POST.get('rid')
        content = request.POST.get('content')
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        print rid
        Replay.objects.filter(id=rid).update(content=content, createtime=now)
        return HttpResponse(json.dumps({'code': 0, 'msg': u'编辑回复成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def best_replay(request):
    try:
        rid = request.GET.get('rid')
        replay_obj = Replay.objects.get(id=rid)
        qid = replay_obj.question_id
        question_obj = Question.objects.get(id=qid)
        print replay_obj.id, question_obj.id
        if question_obj.status == 1:
            return HttpResponse(u'你已经选择了一个最佳答案')
        else:
            replay_obj.best = 1
            question_obj.status = 1
            replay_obj.save()
            question_obj.save()
            return HttpResponse(json.dumps({'code': 0, 'msg': u'选择最佳答案成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def question_list(request):
    """问题详情列表"""
    try:
        pass
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))

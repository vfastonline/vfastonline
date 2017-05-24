#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from vuser.models import User
from vcourse.models import Video
from vpractice.models import Question, QRcomment, Replay, Attention, Repatation, RepaType
from django.db.models import Q, F
from vinform.models import Inform, InformType
from django.conf import settings
from vfast.api import pages
from vcourse.models import Technology
from vfast.templatetags.mytags import time_comp_now

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
            ###print title, desc, video.name, email_status
            try:
                ques = Question.objects.create(title=title, desc=desc, user=user, video=video, createtime=createtime,
                                               email_status=email_status, like=0, dislike=0, status=0, add_repatation=0,
                                               default_repatation=5)
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
            return HttpResponseRedirect('/')
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
        # print replays
        # #print attention, qcomment, replays
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
        ret = Replay.objects.create(content=content, question=question, replay_user=user, like=0, dislike=0,
                                    createtime=time.strftime('%Y-%m-%d %H:%M:%S'), best=0)

        attention = Attention.objects.filter(user=user, question=question).exists()
        if attention:
            type = InformType.objects.get(name='问题回复')
            url = '%s/community/question?qid=%s' % (settings.HOST, question.id)
            Inform.objects.create(color=question.video.course.color, pubtime=time.strftime('%Y-%m-%d %H:%M:%S'),
                                  desc=question.title,
                                  type=type, user=question.user, url=url)

        return HttpResponse(json.dumps({'code': 0, 'rid': ret.id}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def qr_comment(request):
    '''问题回复点赞功能 1为赞, -1为踩'''
    try:
        qid = request.GET.get('qid')
        rid = request.GET.get('rid')
        status = request.GET.get('type')  # 1为赞, -1踩
        status = int(status)
        # print status
        try:
            uid = request.session['user']['id']
            user = User.objects.get(id=uid)
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请先登录'}, ensure_ascii=False))
        if qid and QRcomment.objects.filter(qid=qid, uid=uid).exists():
            return HttpResponse(json.dumps({'code': 0, 'msg': '问题已经评论过'}, ensure_ascii=False))
        elif qid and QRcomment.objects.filter(qid=qid, uid=uid, type='Q').exists() == False:
            QRcomment.objects.create(qid=qid, uid=uid, type='Q', status=status)
            question = Question.objects.get(id=qid)
            if status == 1:
                question.score += 1
                question.like += 1
                question.save()

            else:
                question.score -= 1
                question.dislike -= 1
                question.save()
            return HttpResponse(json.dumps({'code': 0, 'msg': '问题评论成功'}, ensure_ascii=False))
        elif rid and QRcomment.objects.filter(rid=rid, uid=uid, type='R').exists() == False:
            QRcomment.objects.create(rid=rid, uid=uid, type='R', status=status)
            replay = Replay.objects.get(id=rid)
            if status == 1:
                replay.score += 1
                replay.like += 1
                replay.save()
            else:
                replay.score -= 1
                replay.dislike += 1
                replay.save()
                User.objects.filter(id=replay.replay_user_id).filter(repatation=F('repatation') - 1)
                User.objects.filter(id=uid).update(repatation=F('repatation') - 1)
            return HttpResponse(json.dumps({'code': 0, 'msg': '回复评论成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': '回复你已经评论过'}, ensure_ascii=False))
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
        # print status
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请先登录'}))
        if qid and QRcomment.objects.filter(qid=qid, uid=uid, type='Q').exists():
            QRcomment.objects.filter(qid=qid, uid=uid, type='Q').update(status=status)
            question = Question.objects.get(id=qid)
            if status == 1:
                question.score += 2
                question.like += 1
                question.dislike -= 1
                question.save()
                User.objects.filter(id=question.user_id).update(repatation=F('repatation') + 1)
            else:
                question.score -= 2
                question.like -= 1
                question.dislike += 1
                question.save()
                User.objects.filter(id=question.user_id).update(repatation=F('repatation') - 1)
                User.objects.filter(id=uid).update(repatation=F('repatation') - 1)
            return HttpResponse(json.dumps({'code': 0, 'msg': u'修改问题评论成功'}, ensure_ascii=False))
        elif rid and QRcomment.objects.filter(rid=rid, uid=uid, type='R').exists():
            QRcomment.objects.filter(rid=rid, uid=uid, type='R').update(status=status)
            replay = Replay.objects.get(id=rid)
            if status == 1:
                replay.score += 2
                replay.like += 1
                replay.save()
                User.objects.filter(id=replay.replay_user_id).filter(repatation=F('repatation') + 1)
            else:
                replay.score -= 2
                replay.dislike += 1
                replay.save()
                User.objects.filter(id=replay.replay_user_id).filter(repatation=F('repatation') - 1)
                User.objects.filter(id=uid).filter(repatation=F('repatation') - 1)
            return HttpResponse(json.dumps({'code': 0, 'msg': u'修改回复评论成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'ok'}, ensure_ascii=False))
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
            return HttpResponse(json.dumps({'code': 0, 'msg': '取消关注成功'}, ensure_ascii=False))
        elif ret == False and attention == '1':
            Attention.objects.create(qid=qid, uid=uid)
            return HttpResponse(json.dumps({'code': 0, 'msg': '关注成功'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'attention_question , interface right'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def question_detail(request):
    try:
        qid = request.GET.get('qid')
        question = Question.objects.filter(id=qid).values()[0]
        # print question
        return HttpResponse(json.dumps({'question': question}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def replay_detail(request):
    try:
        rid = request.GET.get('rid')
        replay = Replay.objects.filter(id=rid).values()[0]
        # print replay
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
        # print rid, content
        Replay.objects.filter(id=rid).update(content=content, createtime=now)
        return HttpResponse(json.dumps({'code': 0, 'msg': u'编辑回复成功'}))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def question_offer(request):
    """为问题提供悬赏分"""
    try:
        if request.method == "POST":
            qid = request.POST.get('qid')
            repatation = request.POST.get('repatation')
            try:
                uid = request.session['user']['id']
            except:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'用户未登录'}, ensure_ascii=False))
            Question.objects.filter(id=qid).update(add_repatation=repatation, add_repatation_user=uid)
        return HttpResponse(json.dumps({'code': 0, 'msg': u'追加悬赏成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def best_replay(request):
    try:
        rid = request.GET.get('rid')
        replay_obj = Replay.objects.get(id=rid)
        qid = replay_obj.question_id
        question_obj = Question.objects.get(id=qid)
        try:
            uid = request.session['user']['id']
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '用户未登录'}, ensure_ascii=False))
        # print replay_obj.id, question_obj.id
        if question_obj.status == 1:
            return HttpResponse(json.dumps({'code': 0, 'msg': u'你已经选择了一个最佳答案'}, ensure_ascii=False))
        else:
            replay_obj.best = 1
            question_obj.status = 1
            rep = question_obj.default_repatation + question_obj.add_repatation
            replay_obj.save()
            question_obj.save()
            return HttpResponse(json.dumps({'code': 0, 'msg': u'选择最佳答案成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(traceback.format_exc())


def replays(question_id):
    question = Question.objects.get(id=question_id)
    replays = Replay.objects.filter(question=question).count()
    return replays


def question_list(request):
    try:
        techs = Technology.objects.all()
        return render(request, 'Community.html', {'techs': techs})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def question_select(request):
    """问题详情列表"""
    try:
        page = request.GET.get('page', 1)
        type_id = request.GET.get('type', 0)
        order = request.GET.get('order')
        techs = Technology.objects.all()
        print type_id, order
        try:
            userid = request.session['user']['id']
        except:
            return HttpResponse(json.dumps({'code': 1, 'msg': '请先登录'}, ensure_ascii=False))
        if type_id == '0':
            questions = Question.objects.all()
        else:
            questions = Question.objects.filter(video__course__tech_id=type_id)

        if order == 'newer':
            questions = questions.order_by('-createtime')
        elif order == 'hot':
            # 规则重新定义
            pass
        elif order == 'notsolve':
            questions = questions.filter(status=0)
        elif order == 'solved':
            questions = questions.filter(status=1)
        elif order == 'questionbyme':
            questions = questions.filter(user_id=userid)
        else:
            qids = Replay.objects.filter(replay_user_id=userid).values('question_id')
            q = set()
            for qid in qids:
                q.add(qid['question_id'])
            tmp = []
            for question in questions:
                if question.id in q:
                    tmp.append(question)
            questions = tmp
        print questions
        result = []
        current_lines = pages(questions, page, lines=2)
        if len(current_lines) == 0:
            return HttpResponse(json.dumps({'code':0, 'msg':'empty page'}, ensure_ascii=False))
        for item in current_lines:
            question_id =  item.id
            createtime =  time_comp_now(item.createtime)
            title =  item.title
            nickname =  item.user.nickname
            headimg =  item.user.headimg
            video_name =  item.video.name
            tech_name =  item.video.course.tech.name
            tech_color = item.video.course.tech.color
            question_status = item.status
            replay_num = replays(question_id)
            result.append(dict(question_id=question_id, createtime=createtime, title=title, nickname=nickname,
                               headimg=headimg, video_name=video_name, tech_name=tech_name,
                               tech_color=tech_color, question_status=question_status, replay_num=replay_num, ))
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': traceback.format_exc()}, ensure_ascii=False))


def rank_list(request):
    try:
        techs = Technology.objects.all()
        return render(request, 'Community.html', {'techs': techs})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))


def rank_select(request):
    try:
        pass
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1}, ensure_ascii=False))

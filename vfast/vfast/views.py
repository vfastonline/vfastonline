#!encoding:utf-8
from vcourse.models import Course
from django.shortcuts import render
from vcourse.models import Program
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from vcourse.models import Video
from vpractice.models import Timu
from vfast.api import dictfetchall, time_comp_now
from django.conf import settings

import logging
import traceback
import json
import os
import re
from uploader import Uploader


# @require_login()
# @require_role(role=1)
def test(request):
    print 'test'
    # course = connection.cursor()
    # course.execute('select * from vcourse_video')
    # a = dictfetchall(cursor=course)
    return render(request, "detailsQA.html")

def logout(request):
    try:
        del request.session['login']
        del request.session['user']
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')


def index(request):
    try:
        if request.session.get('user'):
            return HttpResponseRedirect('/u/%s' % request.session['user']['id'])
        else:
            return render(request, 'index.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def search_course(request):
    try:
        key_words = request.GET.get('query')
        key_words = key_words.strip()
        vps = Program.objects.all()
        if key_words == '':
            courses = Course.objects.all().values('id')
        else:
            conditions = []
            for i in key_words.split():
                conditions.append("`vcourse_course`.`tag` like BINARY '%%%s%%'" % i)
            sql = "select id from vcourse_course  WHERE (`vcourse_course`.`name` LIKE BINARY '%%%s%%' OR (%s))" % (
                key_words, ' AND '.join(conditions))
            courses = dictfetchall(sql)
        result = []
        for c in courses:
            sql = "select vc.*, vv.vtype, vv.id as video_id, vv.sequence, vp.name as vp_name, vp.color as vp_color from vcourse_program as vp, vcourse_course as vc, vcourse_video as vv where vp.id=vc.tech_id and vv.course_id=vc.id and vc.id=%s order by sequence limit 1" % \
                  c['id']
            try:
                ret = dictfetchall(sql)[0]
                result.append(ret)
            except:
                pass
        tech = request.GET.get('type', None)
        if tech:
            tech_obj = Program.objects.get(name=tech)
            tech_id = tech_obj.id
            tmp = [course for course in result if course['tech_id'] == tech_id]
            result = tmp
            return render(request, 'search_Result.html',
                          {'results': result, 'vps': vps, 'xingxing': [0, 1, 2, 3, 4], 'tech_obj': tech_obj,
                           'key_words': key_words})
        elif len(result) != 0:
            return render(request, 'search_Result.html',
                          {'results': result, 'vps': vps, 'xingxing': [0, 1, 2, 3, 4], 'desc': '',
                           'key_words': key_words})
        else:
            return render(request, 'search_Result.html', {'key_words': key_words, 'vps': vps})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def search_js(request):
    try:
        course_names = Course.objects.all().values('name')
        cnames = [item['name'] for item in course_names]
        return HttpResponse(json.dumps({'name': cnames}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


def playVideo(request, params):
    try:
        video_obj = Video.objects.get(id=int(params))
        try:
            userid = request.session['user']['id']
        except:
            return render(request, 'playVideo.html')
        sql = """select vv.id, vv.name, vv.notes, vv.vurl, vv.vtype, vw.user_id, vv.vtype_url, vv.vtime, vv.course_id,  vw.status from  vcourse_video  as vv left join vrecord_watchrecord as vw  on  vv.id=vw.video_id and vw.user_id=%s where vv.course_id=%s""" % (
            userid, video_obj.course.id)
        videos = dictfetchall(sql)
        sql_video_process = "select video_process from vrecord_watchrecord where user_id = %s and video_id =%s;" % (
            userid, video_obj.id)
        ret = dictfetchall(sql_video_process)
        try:
            video_process = ret[0]['video_process']
        except:
            video_process = 0
        q_sql = 'select vp.*, vu.username from vpractice_question as vp, vuser_user as vu where video_id=%s and vu.id=vp.user_id order by createtime desc;' % int(
            params)
        questions = dictfetchall(q_sql)
        for item in questions:
            item['createtime'] = '%s%s' % (time_comp_now(item['createtime']), '提问')
            r_sql = 'select count(1) as replay from vpractice_replay where question_id = %s;' % item['id']
            res = dictfetchall(r_sql)[0]
            item['replay'] = res['replay']
        return render(request, 'playVideo.html',
                      {'videos': videos, 'video_obj': video_obj, 'video_process': video_process,
                       'questions': questions})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(status=404)


def practice(request, params):
    try:
        video_obj = Video.objects.get(id=int(params))
        try:
            userid = request.session['user']['id']
        except:
            return render(request, 'playVideo.html')
        sql = """select vv.id, vv.name, vv.notes, vv.vurl, vv.vtype, vw.user_id, vv.vtype_url, vv.vtime, vv.course_id,  vw.status from  vcourse_video  as vv left join vrecord_watchrecord as vw  on  vv.id=vw.video_id and vw.user_id=%s where vv.course_id=%s""" % (
            userid, video_obj.course.id)
        videos = dictfetchall(sql)
        sql_video_process = "select video_process from vrecord_watchrecord where user_id = %s and video_id =%s;" % (
            userid, video_obj.id)
        ret = dictfetchall(sql_video_process)
        try:
            video_process = ret[0]['video_process']
        except:
            video_process = 0
        q_sql = 'select vp.*, vu.username from vpractice_question as vp, vuser_user as vu where video_id=%s and vu.id=vp.user_id order by createtime desc;' % int(
            params)
        questions = dictfetchall(q_sql)
        for item in questions:
            item['createtime'] = '%s%s' % (time_comp_now(item['createtime']), '提问')
            r_sql = 'select count(1) as replay from vpractice_replay where question_id = %s;' % item['id']
            res = dictfetchall(r_sql)[0]
            item['replay'] = res['replay']

        ####重看一遍 上个视频的URL
        sql_replay = 'select id, sequence, end, vtype from vcourse_video where course_id=%s and sequence = %s;' % (
            video_obj.course_id, video_obj.sequence - 1)
        ret_replay = dictfetchall(sql_replay)
        if len(ret_replay) != 0:
            replay_url = '/video/%s/' % ret_replay[0]['id'] if ret_replay[0]['vtype'] == 0 else '/practice/%s/' % \
                                                                                                ret_replay[0]['id']
        else:
            replay_url = False
        ####跳过问题 下个视频的URL, 如果没有下个视频, 按钮不显示
        sql_skip = 'select id, sequence, end, vtype from vcourse_video where course_id=%s and sequence = %s;' % (
            video_obj.course_id, video_obj.sequence + 1)
        ret_skip = dictfetchall(sql_skip)
        if len(ret_skip) == 0:
            skip_url = False
        else:
            skip_url = '/video/%s/' % ret_skip[0]['id'] if ret_skip[0]['vtype'] == 0 else '/practice/%s/' % ret_skip[0][
                'id']
        ####下一题,  获取下一个题目,如果没有下一个题目了, 按钮不显示
        timus = Timu.objects.filter(video=video_obj).values()
        return render(request, 'question.html',
                      {'videos': videos, 'video_obj': video_obj, 'video_process': video_process, 'questions': questions,
                       'replay_url': replay_url,
                       'skip_url': skip_url, 'timus': timus})
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(status=404)


def upload(request):
    """UEditor文件上传接口
    config 配置文件
    result 返回结果
    """
    result = {}
    action = request.GET.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(settings.BASE_DIR, 'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    # print CONFIG
    # print action
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }

        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }

        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        # print fieldName, request.FILES.get('upfile')
        if fieldName in request.FILES:
            field = request.FILES[fieldName]
            # print field.name, field.size,
            uploader = Uploader(field, config, os.path.join(settings.BASE_DIR))
            result = uploader.getFileInfo()
        else:
            result['state'] = 'upload interface error'

    # elif action in ('uploadscrawl'):
    #     # 涂鸦上传
    #     fieldName = CONFIG.get('scrawlFieldName')
    #     config = {
    #         "pathFormat": CONFIG.get('scrawlPathFormat'),
    #         "maxSize": CONFIG.get('scrawlMaxSize'),
    #         "allowFiles": CONFIG.get('scrawlAllowFiles'),
    #         "oriName": "scrawl.png"
    #     }
    #     if fieldName in request.form:
    #         field = request.form[fieldName]
    #         uploader = Uploader(field, config, app.static_folder, 'base64')
    #         result = uploader.getFileInfo()
    #     else:
    #         result['state'] = '上传接口出错'
    #
    # elif action in ('catchimage'):
    #     config = {
    #         "pathFormat": CONFIG['catcherPathFormat'],
    #         "maxSize": CONFIG['catcherMaxSize'],
    #         "allowFiles": CONFIG['catcherAllowFiles'],
    #         "oriName": "remote.png"
    #     }
    #     fieldName = CONFIG['catcherFieldName']
    #     if fieldName in request.form:
    #         # 这里比较奇怪，远程抓图提交的表单名称不是这个
    #         source = []
    #     elif '%s[]' % fieldName in request.form:
    #         # 而是这个
    #         source = request.form.getlist('%s[]' % fieldName)
    #     _list = []
    #     for imgurl in source:
    #         uploader = Uploader(imgurl, config, app.static_folder, 'remote')
    #         info = uploader.getFileInfo()
    #         _list.append({
    #             'state': info['state'],
    #             'url': info['url'],
    #             'original': info['original'],
    #             'source': imgurl,
    #         })
    #     result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
    #     result['list'] = _list

    else:
        result['state'] = 'request URL error'

    # print result
    result = json.dumps(result)
    if 'callback' in request.GET:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback args is not right'}, ensure_ascii=False)
    # print result
    # res.mimetype = mimetype
    # res.headers['Access-Control-Allow-Origin'] = '*'
    # res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return HttpResponse(result)

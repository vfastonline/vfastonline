#!encoding: utf-8
from vuser.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from vfast.api import require_login
import urllib
import json
import logging
import traceback


GITHUB_AUTHORIZE_URL = settings.GITHUB_AUTHORIZE_URL
GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK


# Create your views here.
def _get_refer_url(request):
    refer_url = request.META.get('HTTP_REFER', '/')
    host = request.META.get("HTTP_HOST")
    if refer_url.startswith('http') and host not in refer_url:
        refer_url = '/'
    return refer_url


# 第一步, 请求github第三方登陆
@require_login()
def github_login(request):
    uid = request.session['user']['id']
    data = {
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'redirect_uri': GITHUB_CALLBACK+'?uid=%s' % uid,
        'state': _get_refer_url(request),
    }
    github_auth_url = '%s?%s' % (GITHUB_AUTHORIZE_URL, urllib.urlencode(data))
    # print github_auth_url
    return HttpResponseRedirect(github_auth_url)


# github回调,获取需要的信息
def github_auth(request):
    try:
        if 'code' not in request.GET:
            return render(request, 'index.html')
        code = request.GET.get('code')
        uid = request.GET.get('uid')
        logging.getLogger().error('code:%s  uid: %s' % (code, uid))
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': GITHUB_CLIENTID,
            'client_secret': GITHUB_CLIENTSECRET,
            'code': code,
            'redirect_uri': GITHUB_CALLBACK,
        }
        data = urllib.urlencode(data)

        # 设置请求返回的数据类型
        headers = {'Accept': 'application/json'}

        req = urllib.urlopen(url, data, headers)
        result = req.read()
        access_token = result.split('&')[0].split('=')[1]

        url_token = 'https://api.github.com/user?access_token=%s' % access_token
        response = urllib.urlopen(url_token)
        html = response.read()
        html = json.loads(html)
        repos_url = html['repos_url']
        html_url = html['html_url']
        User.objects.filter(id=uid).update(githuburl=html_url, githubrepo=repos_url)
        # return HttpResponse(json.dumps({'code':0, 'msg':u'github验证成功'}, ensure_ascii=False))
        return HttpResponseRedirect("/u/editpage")
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code':1}))



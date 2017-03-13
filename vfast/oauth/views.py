#!encoding: utf-8
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import urllib
import json

GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_CLIENTID = 'b758723e0c76d63dc514'
GITHUB_CLIENTSECRET = '529eeba7bafd22682ca91e6bfffd49ebf2383076'
GITHUB_CALLBACK = 'http://127.0.0.1:8000/github_auth'


# Create your views here.
def _get_refer_url(request):
    refer_url = request.META.get('HTTP_REFER', '/')
    host = request.META.get("HTTP_HOST")
    if refer_url.startswith('http') and host not in refer_url:
        refer_url = '/'
    return refer_url


# 第一步, 请求github第三方登陆
def github_login(request):
    data = {
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'redirect_uri': GITHUB_CALLBACK,
        'state': _get_refer_url(request),
    }
    github_auth_url = '%s?%s' % (GITHUB_AUTHORIZE_URL, urllib.urlencode(data))
    print github_auth_url
    return HttpResponseRedirect(github_auth_url)


# github回调,获取需要的信息
def github_auth(request):
    if 'code' not in request.GET:
        return render(request, 'index.html')
    code = request.GET.get('code')
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'code': code,
        'redirect_uri': GITHUB_CALLBACK,
    }
    data = urllib.urlencode(data)

    binary_data = data.encode('utf-8')
    print data

    # 设置请求返回的数据类型
    headers = {'Accept': 'application/json'}

    req = urllib.urlopen(url, data, headers)
    result = req.read()
    print result
    # result = json.loads(result)
    access_token = result.split('&')[0].split('=')[1]

    url_token = 'https://api.github.com/user?access_token=%s' % access_token
    print  url_token
    response = urllib.urlopen(url_token)
    html = response.read()
    html = json.loads(html)
    repos_url = html['repos_url']
    print repos_url
    rep = urllib.urlopen(repos_url)
    rep = json.loads(rep.read())
    repos_list = [item['html_url'] for item in rep]
    print repos_list  # 获取用户的repos
    # return HttpResponse('oAuth, ok~!')
    return HttpResponseRedirect('/')

# {"login": "sky-dadan", "id": 17780632, "avatar_url": "https://avatars2.githubusercontent.com/u/17780632?v=3",
#  "gravatar_id": "", "url": "https://api.github.com/users/sky-dadan", "html_url": "https://github.com/sky-dadan",
#  "followers_url": "https://api.github.com/users/sky-dadan/followers",
#  "following_url": "https://api.github.com/users/sky-dadan/following{/other_user}",
#  "gists_url": "https://api.github.com/users/sky-dadan/gists{/gist_id}",
#  "starred_url": "https://api.github.com/users/sky-dadan/starred{/owner}{/repo}",
#  "subscriptions_url": "https://api.github.com/users/sky-dadan/subscriptions",
#  "organizations_url": "https://api.github.com/users/sky-dadan/orgs",
#  "repos_url": "https://api.github.com/users/sky-dadan/repos",
#  "events_url": "https://api.github.com/users/sky-dadan/events{/privacy}",
#  "received_events_url": "https://api.github.com/users/sky-dadan/received_events", "type": "User", "site_admin": false,
#  "name": "sky-dadan", "company": null, "blog": null, "location": null, "email": null, "hireable": null, "bio": null,
#  "public_repos": 4, "public_gists": 0, "followers": 0, "following": 0, "created_at": "2016-03-11T09:27:37Z",
#  "updated_at": "2017-01-13T05:40:55Z"}

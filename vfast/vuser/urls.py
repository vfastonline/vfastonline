#!encoding:utf-8
from django.conf.urls import url
from vuser import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^exists', views.userexists),
    url(r'^register', views.register, name='register'),
    url(r'^active', views.useractive, name='useractive'),
    url(r'^resetpw', views.reset_password, name='resetpw'),
    url(r'^login', views.login, name='login'),
    url(r'^detail', views.userdetail, name='userdetail'),
    url(r'^(\d+)/$', views.dashboard, name='dashboard'),
    url(r'^follow', views.follow_people, name='follow'),
    url(r'^model', views.user_model, name='usermodel'),
    url(r'^person', views.person_page),
    url(r'^is_open$', views.is_open),
    url('^editpage/change_headimg$', views.change_headimg, name='change_heading'),
    url('^editpage/default_headimg$', views.default_headimg, name='default_headimg'),
    url('^editpage/github$', views.github, name='github'),
    url('^editpage$', views.editpage),
    url('^editpage/nickname$', views.nikcname),
    url('^editpage/editelse', views.editelse),
]
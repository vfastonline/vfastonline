#!encoding:utf-8
from django.conf.urls import url
from vuser import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^exists', views.userexists),
    url(r'^register', views.register, name='register'),
    url(r'^resetpw', views.reset_password, name='resetpw'),
    url(r'^login', views.login, name='login'),
    url(r'^detail', views.userdetail, name='userdetail'),
    url(r'^(\d+)/$', views.dashboard, name='dashboard'),
    url(r'^follow', views.follow_people, name='follow'),
    url(r'^model', views.user_model, name='usermodel'),
    url(r'^person', views.person_page),
    url(r'^is_open$', views.is_open),
    url(r'editpage/change_headimg$', views.change_headimg, name='change_heading'),
    url(r'editpage/default_headimg$', views.default_headimg, name='default_headimg'),
    url(r'editpage/github$', views.github, name='github'),
    url(r'editpage$', views.editpage),
    url(r'editpage/nickname$', views.nikcname),
    url(r'editpage/editelse$', views.editelse),
    url(r'editpage/resetpw$', views.reset_password, name='resetpw'),
    url(r'editpage/personpage$', views.personpage),
    url(r'^phonecode$',views.phone_code, name='phone_code'),
    url(r'^userimage$', views.userimage, name='userimage'),
    url(r'editpage/resetphone$', views.user_phone, name='resetphone'),
    url(r'^ucenter$', views.ucenter, name='ucenter'),
    url(r'^uinfo', views.uinfo, name='uinfo'),
    url(r'^uplan$', views.uplan, name='uplan'),
]
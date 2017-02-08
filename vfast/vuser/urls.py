#!encoding:utf-8
from django.conf.urls import url
from vuser import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^exist', views.userexists),
    url(r'^register', views.register, name='register'),
    url(r'^active', views.useractive, name='useractive'),
    url(r'^resetpw', views.resetpw, name='resetpw'),
    url(r'^resetpassword', views.resetpwd_verify, name='resetpwd_verify'),
    url(r'^login', views.login, name='login'),
    url(r'^detail', views.userdetail, name='userdetail'),

]
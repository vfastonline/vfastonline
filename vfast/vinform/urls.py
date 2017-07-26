#!encoding:utf-8
from django.conf.urls import url
from vinform import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^create_info', views.create_info_user,),
    url(r'^getinfo$', views.getinfo,),
    url(r'^dall$', views.del_all_info_user),
    url(r'^done$', views.del_info_user,),
    url(r'^create_feedback$', views.create_feedback),
    url(r'^daily_mail$', views.daily_mail)
]
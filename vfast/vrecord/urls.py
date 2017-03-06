#!encoding:utf-8
from django.conf.urls import url
from vrecord import views

urlpatterns = [
    url(r'^video', views.record_video, name='recordvideo'),
    url(r'^weekscore', views.get_score_seven_day, name='weekscore'),
]
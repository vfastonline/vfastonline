#!encoding:utf-8
from django.conf.urls import url
from record import views

urlpatterns = [
    url(r'^video', views.record_video, name='recordvideo'),
    url(r'^score', views.record_score, name='recordscore'),
]
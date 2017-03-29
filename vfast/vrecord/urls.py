#!encoding:utf-8
from django.conf.urls import url
from vrecord import views

urlpatterns = [
    url(r'^video', views.record_video, name='recordvideo'),
    url(r'^weekscore', views.get_score_seven_day, name='weekscore'),
    url(r'^monthscore', views.get_score_thirty_day, name='monthscore'),
    url(r'^techscore', views.sum_score_tech, name='techscore'),
]
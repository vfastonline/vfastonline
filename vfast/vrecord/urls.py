#!encoding:utf-8
from django.conf.urls import url
from vrecord import views

urlpatterns = [
    url(r'^video', views.record_video, name='recordvideo'),
    url(r'^weekscore', views.get_score_seven_day, name='weekscore'),
    url(r'^monthscore', views.get_score_thirty_day, name='monthscore'),
    url(r'^test$', views.test, name='get_track_badge'),
    url(r'^timu$', views.record_timu, name='record_timu'),
    url(r'^face$', views.face),
    url(r'^getface', views.getface),
]


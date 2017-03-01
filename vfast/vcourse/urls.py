#!encoding:utf-8
from django.conf.urls import url
from vcourse import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^cadd', views.course_add, name='cadd'),
    url(r'^vadd', views.video_add, name='vadd'),
    url(r'^padd', views.path_add, name='padd'),
    url(r'^video', views.play_video, name='getvideo'),
    url(r'^courses$', views.getcourses, name='courses'),
    url(r'^course$', views.getcourse, name='course_detail'),
    url(r'^tracks$', views.getpaths, name='getpaths'),
    url(r'^track$', views.getpath, name='getpath'),
    url(r'^join_track$', views.join_path, name='joinpath'),
]
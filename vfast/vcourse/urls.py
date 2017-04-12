#!encoding:utf-8
from django.conf.urls import url
from vcourse import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^courses$', views.getcourses, name='courses'),
    url(r'^tracks$', views.getpaths, name='getpaths'),
    url(r'^track$', views.getpath, name='getpath'),
    url(r'^join_track$', views.join_path, name='joinpath'),
]
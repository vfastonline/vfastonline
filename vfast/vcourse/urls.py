#!encoding:utf-8
from django.conf.urls import url
from vcourse import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^cadd', views.course_add, name='cadd'),
    url(r'^vadd', views.video_add, name='vadd'),
    url(r'^padd', views.path_add, name='padd'),
    url(r'^video', views.getvideo, name='getvideo'),
    url(r'^course', views.getcourse, name='getcourse'),
    url(r'^path', views.getpath, name='getpath'),
    url(r'^list', views.getcourses, name='courselist'),
]
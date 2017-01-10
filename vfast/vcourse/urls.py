#!encoding:utf-8
from django.conf.urls import url
from vcourse import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^courseadd', views.course_add, name='courseadd'),
    url(r'^videoadd', views.video_add, name='videoadd'),
    url(r'^pathadd', views.path_add, name='pathadd'),
    url(r'^video', views.getvideo, name='getvideo'),
    url(r'^course', views.getcourse, name='getcourse'),
    url(r'^path', views.getpath, name='getpath'),
    url(r'^list', views.getcourseall, name='courselist'),

]
#!encoding:utf-8
from django.conf.urls import url
from vgrade import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^hfadd', views.headframe_add, name='hframeadd'),
    url(r'^hadd', views.headimg_add, name='headadd'),
]
#!encoding:utf-8
from django.conf.urls import url
from vuser import views

urlpatterns = [
    url(r'^test', views.test),
]
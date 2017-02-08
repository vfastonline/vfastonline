#!encoding:utf-8
from django.conf.urls import url
from badge import views

urlpatterns = [
    url(r'^add', views.badge_add, name='badgeadd'),
    url(r'^get', views.badge_get, name='badgeget'),
    # url(r'^test', views.test),

]
#!encoding:utf-8
from django.conf.urls import url
from vinspect import views

urlpatterns = [
    url(r'^(\d+)/', views.inspect_detail, name='inspect_detail'),
    url(r'^result$', views.inspect_result),
    url(r'^list$', views.inspect_list),
]
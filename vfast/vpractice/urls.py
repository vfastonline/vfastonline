#!encoding:utf-8
from django.conf.urls import url
from vpractice import views

urlpatterns = [
    url(r'question', views.show_question, name='show_question'),
    url(r'qcomment', views.question_comment),
]
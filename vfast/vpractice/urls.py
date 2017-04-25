#!encoding:utf-8
from django.conf.urls import url
from vpractice import views

urlpatterns = [
    url(r'^question$', views.show_question, name='show_question'),
    url(r'^qrcomment$', views.qr_comment),
    url(r'^update_qrcomment$', views.update_comment, name='update_qrcomment'),
    url(r'^attention$', views.attention_question, name='attention_question'),
    url(r'^replay$', views.add_replay, name='replay'),
    url(r'^update_question$', views.update_question, name='update_question'),
    url(r'^update_replay$',views.update_replay, name='update_replay'),
    url(r'^best_replay$', views.best_replay, name='best_replay'),
]
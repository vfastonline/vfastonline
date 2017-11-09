#!encoding:utf-8
from django.conf.urls import url
from vresume.views import *

urlpatterns = [
    url(r'^(?P<resume_type>\w+)/add$', ResumeAdd.as_view()),
    url(r'^(?P<resume_type>\w+)/(?P<pk>[0-9]+)/delete$', ResumeDelete.as_view()),
    url(r'^(?P<id>\w+)/detail$', ResumeDetail.as_view()),
    url(r'^(?P<resume_type>\w+)/(?P<pk>[0-9]+)/update$', ResumeUpdate.as_view()),
]

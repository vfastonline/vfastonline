#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models

from vcourse.models import Course, Path
from vuser.models import User


class Badge(models.Model):
    badgename = models.CharField('勋章名称', max_length=100, unique=True)
    large_url = models.FileField('大勋章', upload_to='badge')
    small_url = models.FileField('小位置', upload_to='badge')
    createtime = models.DateField('勋章创建时间', auto_now=True)
    course = models.ForeignKey(Course, null=True, blank=True, verbose_name='课程勋章')
    description = models.TextField(verbose_name='勋章内容简介', default='')
    path = models.ForeignKey(Path, null=True, blank=True, verbose_name='路线勋章')

    def __unicode__(self):
        return self.badgename

    class Meta:
        verbose_name = "勋章"


class UserBadge(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='用户ID')
    badge = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='勋章ID')
    createtime = models.CharField('勋章获取时间', max_length=20)

    def __unicode__(self):
        return self.user.nickname

    class Meta:
        verbose_name = "用户勋章"

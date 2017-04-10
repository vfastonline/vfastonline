#!encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from vcourse.models import Course
from vuser.models import User


# Create your models here.
class Badge(models.Model):
    badgename = models.CharField('勋章名称', max_length=100, null=True, blank=True, default=' ')
    badgeurl = models.ImageField('勋章位置', upload_to='badge')
    createtime = models.DateField('勋章创建时间', auto_now=True)
    course = models.ForeignKey(Course, null=True, blank=True)

    def __unicode__(self):
        return self.badgename


class UserBadge(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='用户ID')
    badge = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='勋章ID')
    createtime = models.CharField('勋章获取时间', max_length=20)

    def __unicode__(self):
        return self.userid.username

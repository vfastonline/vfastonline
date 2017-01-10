#!encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from vcourse.models import Course
from vuser.models import User


# Create your models here.
class Badge(models.Model):
    badgename = models.CharField('勋章名称', max_length=100, null=True, blank=True, default=' ')
    badgeurl = models.CharField('勋章图片位置', max_length=100, null=True, blank=True, default=' ')
    createtime = models.DateTimeField('勋章创建时间')
    cid = models.ForeignKey(Course)

    def __unicode__(self):
        return self.badgename


class UserBadge(models.Model):
    userid = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='用户ID')
    badgeid = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='勋章ID')
    gain_time = models.DateTimeField('勋章获取时间')

    def __unicode__(self):
        return self.userid.username

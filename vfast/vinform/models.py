#!encoding: utf-8
from __future__ import unicode_literals
from django.db import models
from vuser.models import User


# Create your models here.
class InformType(models.Model):
    name = models.CharField(verbose_name='类型名称', max_length=20)

    def __unicode__(self):
        return self.name


class InformTask(models.Model):
    type = models.ForeignKey(InformType)
    color = models.CharField(verbose_name='通知颜色', max_length=15, blank=True, null=True, default='')
    pubtime = models.DateField(verbose_name='任务发布时间')
    desc = models.CharField(verbose_name='简介', max_length=100, default='')
    url = models.CharField(verbose_name='跳转URL', max_length=100, default='')

    def __unicode__(self):
        return self.url


class Inform(models.Model):
    STATUS = (
        (0, '未读'),
        (1, '已读'),
    )
    infor = models.ForeignKey(InformTask, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    status = models.IntegerField(verbose_name='通知状态', choices=STATUS, default=0)

    def __unicode__(self):
        return self.user.nickname
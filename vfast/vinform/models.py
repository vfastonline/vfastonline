#!encoding: utf-8
from __future__ import unicode_literals

import django.utils.timezone as timezone
from django.db import models

from vuser.models import User


class InformType(models.Model):
    name = models.CharField(verbose_name='类型名称', max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "通知类型"
        verbose_name_plural = "通知类型"


class InformTask(models.Model):
    STATUS = (
        (0, '未完成'),
        (1, '已完成'),
    )
    type = models.ForeignKey(InformType, verbose_name="通知类型")
    color = models.CharField(verbose_name='通知颜色', max_length=15, blank=True, null=True, default='')
    pubtime = models.DateTimeField(verbose_name='任务发布时间')
    desc = models.CharField(verbose_name='简介', max_length=100, default='')
    url = models.CharField(verbose_name='跳转URL', max_length=100, default='')
    status = models.IntegerField(verbose_name='状态', choices=STATUS)  # 0任务为通知, 1任务已通知

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = "通知任务"
        verbose_name_plural = "通知任务"


class Inform(models.Model):
    STATUS = (
        (0, '未读'),
        (1, '已读'),
    )
    type = models.ForeignKey(InformType, verbose_name="通知类型")
    user = models.ForeignKey(User, models.CASCADE)
    color = models.CharField(verbose_name='通知颜色', max_length=15, blank=True, null=True, default='')
    pubtime = models.DateTimeField(verbose_name='任务发布时间', default=timezone.now)
    desc = models.CharField(verbose_name='简介', max_length=100, default='')
    url = models.CharField(verbose_name='跳转URL', max_length=100, default='')

    def __unicode__(self):
        return self.user.nickname

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知"


class Feedback(models.Model):
    user = models.ForeignKey(User, verbose_name="最终用户")
    description = models.TextField(verbose_name='用户反馈内容')
    createtime = models.CharField(verbose_name='用户反馈时间', max_length=19, null=True, blank=True)
    userip = models.CharField(verbose_name='用户ip', max_length=15)
    user_agent = models.TextField()

    def __unicode__(self):
        return self.user.nickname

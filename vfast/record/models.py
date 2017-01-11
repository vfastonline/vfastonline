#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from vuser.models import User
from vcourse.models import Course, Video


# Create your models here.
class Score(models.Model):
    createtime = models.DateField('获得积分的日期')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name='课程ID', blank=True)
    score = models.IntegerField('获得积分')

    def __unicode__(self):
        return self.user.username


class WatchRecord(models.Model):
    STATUS = (
        (0, '已看完'),
        (1, '未看完')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, verbose_name='视频ID')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
    video_progress = models.IntegerField('观看时间进度')
    status = models.IntegerField('观看状态', choices=STATUS)
    recordtime = models.DateTimeField('记录时间')

    def __unicode__(self):
        return self.user.username

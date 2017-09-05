#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from vuser.models import User
from vcourse.models import Course, Video, Technology


# Create your models here.
class Score(models.Model):
    """用户得分记录表"""
    createtime = models.CharField('获得积分的日期', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, null=True, verbose_name='类别ID', blank=True)
    score = models.IntegerField('获得积分')

    def __unicode__(self):
        return self.user.nickname


class WatchRecord(models.Model):
    """用户观看记录表"""
    STATUS = (
        (0, '已看完'),
        (1, '未看完')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, verbose_name='视频ID')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
    video_process = models.IntegerField('观看时间进度')
    video_time = models.IntegerField('视频长度', default=0)
    status = models.IntegerField('观看状态', choices=STATUS)
    createtime = models.CharField('记录时间', max_length=20)

    def __unicode__(self):
        return self.user.nickname


class WatchCourse(models.Model):
    """记录用户那些课程都已经观看完成"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
    createtime = models.CharField('记录时间', max_length=20, default='2015-09-08 12:00:00')


class Watchtime(models.Model):
    """记录用户观看视频时长"""
    createtime = models.CharField('日期', max_length=10)
    userid = models.IntegerField('用户ID')
    time = models.IntegerField('学习时长')


class WatchTimu(models.Model):
    """记录用户习题情况"""
    createtime = models.CharField('日期', max_length=10)
    userid = models.IntegerField('用户ID')
    timuid = models.IntegerField('题目ID')
    courseid = models.IntegerField('课程ID')
    status = models.CharField(verbose_name='习题状态', max_length=1)   #0正确, 1错误




#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from vuser.models import User

# Create your models here.
class CourseType(models.Model):
    typename = models.CharField('课程分类技术', max_length=50)

    def __unicode__(self):
        return self.typename


class CourseClass(models.Model):
    classname = models.CharField('课程分类功能', max_length=50)

    def __unicode__(self):
        return self.classname


class Course(models.Model):
    PUB_STATUS = (
        (0, '即将发布'),
        (1, '已发布'),
        (2, '默认')
    )
    name = models.CharField('课程名称', max_length=50)
    desc = models.CharField('课程描述', max_length=1000, null=True, blank=True, default=' ')
    totaltime = models.CharField('课程总时长', max_length=50, null=True, blank=True, default=' ')
    difficult = models.IntegerField('课程难度', null=True, blank=True)
    type = models.ForeignKey(CourseType, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='语言分类')
    cl =  models.ForeignKey(CourseClass, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='功能分类')
    color = models.CharField('颜色', max_length=30, null=True, blank=True)
    pubstatus = models.IntegerField('发布状态', choices=PUB_STATUS, null=True, default=2)
    subscibe = models.IntegerField('学习课程人数', null=True, blank=True)
    order = models.IntegerField('课程顺序', unique=True)

    def __unicode__(self):
        return self.name


class Path(models.Model):
    name = models.CharField('路线名称', max_length=50)
    desc = models.CharField('路线简介', max_length=1000, blank=True, null=True, default=' ')
    introvideourl = models.CharField('路线介绍视频', max_length=100, blank=True, null=True, default=' ')
    jobscount = models.IntegerField('岗位数', null=True, blank=True, default=5555)
    salary = models.CharField('岗位起薪', null=True, blank=True, max_length=50, default=' ')
    jobtime = models.DateField('岗位&起薪统计时间', null=True, blank=True)
    difficult = models.IntegerField('路径难度', null=True, blank=True)
    pathimg = models.CharField('路线展示图片', null=True, blank=True, default=' ', max_length=100)
    totaltime = models.CharField('路线总时间', null=True, blank=True, default=' ', max_length=50)
    subscibe = models.IntegerField('参加路线人数', null=True, blank=True)
    course = models.ManyToManyField(Course, verbose_name='路线包含的课程')

    def __unicode__(self):
        return self.name


class Video(models.Model):
    name = models.CharField('视频名称', max_length=100)
    time = models.IntegerField('视频时长')
    location = models.CharField('视频存放位置', max_length=100)
    subtitle = models.CharField('字幕存放位置', max_length=100)
    order = models.IntegerField('视频播放顺序', unique=True)
    teacher_note = models.CharField('讲师笔记', max_length=100, default=' ', null=True, blank=True)
    appraise = models.IntegerField('总评星', null=True, blank=True, default=0)
    teacher = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='讲师ID')
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
    watchpeople = models.IntegerField('观看视频人数', null=True, blank=True, default=0)

    def __unicode__(self):
        return self.name

#
# class Score(models.Model):
#     createtime = models.DateField('获得积分的日期')
#     userid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
#     courseid = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name='课程ID')
#     score = models.IntegerField('获得积分')
#
#     def __unicode__(self):
#         return self.userid.username
#
#
# class WatchRecord(models.Model):
#     STATUS = (
#         (0, '已看完'),
#         (1, '未看完')
#     )
#     userid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
#     videoid = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, verbose_name='视频ID')
#     courseid = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
#     video_progress = models.IntegerField('观看时间进度')
#     status = models.IntegerField('观看状态', choices=STATUS)
#     recordtime = models.BigIntegerField('记录时间')
#
#     def __unicode__(self):
#         return self.userid.username



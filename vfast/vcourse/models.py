#!encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from vuser.models import User


# Create your models here.
class Program(models.Model):
    name = models.CharField('技术类别', max_length=50)
    color = models.CharField('颜色', max_length=10, default='#FFFFFF')

    def __unicode__(self):
        return self.name




class Course(models.Model):
    PUB_STATUS = (
        (0, '已发布'),
        (1, '即将发布'),
        (2, '默认')
    )
    ICON_STATUS = (
        (0, '视频'),
        (1, '题库'),
        (2, '项目')
    )
    name = models.CharField('课程名称', max_length=50)
    desc = models.TextField('课程描述', null=True, blank=True, default=' ')
    totaltime = models.CharField('课程总时长', max_length=50, null=True, blank=True, default=' ')
    difficult = models.IntegerField('课程难度', null=True, blank=True, default=4)
    tech = models.ForeignKey(Program, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='技术分类')
    icon = models.IntegerField('课程对应的图标', choices=ICON_STATUS, default=0)
    icon_url = models.CharField('课程图标URL', max_length=50, default=' ', null=True)
    color = models.CharField('颜色', max_length=30, null=True, blank=True)
    pubstatus = models.IntegerField('发布状态', choices=PUB_STATUS, null=True, default=2)
    subscibe = models.IntegerField('学习课程人数', null=True, blank=True, default=0)
    createtime = models.CharField('课程创建时间', max_length=20)
    teach = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='作者')
    people = models.IntegerField('学习课程的人数', default=500)
    pubdate = models.CharField('课程发布时间', max_length=50, default='即将发布')

    def __unicode__(self):
        return self.name


class Path(models.Model):
    name = models.CharField('路线名称', max_length=50)
    desc = models.CharField('路线简介', max_length=1000, blank=True, null=True, default=' ')
    intrv = models.CharField('路线介绍视频', max_length=100, blank=True, null=True, default=' ')
    jobscount = models.CharField('岗位数', null=True, blank=True, default=' ', max_length=20)
    salary = models.CharField('岗位起薪', null=True, blank=True, max_length=50, default=' ')
    jstime = models.CharField('岗位&起薪统计时间', null=True, blank=True, max_length=50)
    difficult = models.IntegerField('路径难度', null=True, blank=True)
    pathimg = models.CharField('路线展示图片', null=True, blank=True, default=' ', max_length=100)
    pathwel = models.CharField('路线介绍页面图面', null=True, blank=True, default=' ', max_length=100)
    totaltime = models.CharField('路线总时间', null=True, blank=True, default=' ', max_length=50)
    subscibe = models.IntegerField('参加路线人数', null=True, blank=True)
    createtime = models.CharField('路线创建时间', max_length=20)
    orders = models.CharField('课程顺序', null=True, blank=True, max_length=30)
    color = models.CharField('路线颜色', null=True, blank=True, max_length=30, default='red')
    avrage_salary = models.CharField('平均入门薪水', max_length=10, null=True, blank=True, default='1W')


    def __unicode__(self):
        return self.name


class Video(models.Model):
    VTYPE = (
        (0, '视频'),
        (1, '题目'),
    )
    name = models.CharField('视频名称', max_length=100)
    vtime = models.IntegerField('视频时长')
    vurl = models.CharField('视频存放位置', max_length=100)
    cc = models.CharField('字幕存放位置', max_length=100)
    notes = models.CharField('讲师笔记', max_length=100, default=' ', null=True, blank=True)
    score = models.IntegerField('总评星', null=True, blank=True, default=0)
    scorepeople = models.IntegerField('评星人数', null=True, blank=True, default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
    watched = models.IntegerField('观看视频人数', null=True, blank=True, default=0)
    createtime = models.CharField('视频上传时间', max_length=20, null=True, blank=True)
    end = models.IntegerField('是否为最后一节视频', default=0)  #0不是, 1是
    vtype = models.IntegerField('类型, 视频, 题目', default=0)
    vtype_url = models.CharField('类型图标', max_length=50, default='/static/svg/video.svg')
    order = models.IntegerField('视频播放顺序', default=0)

    def __unicode__(self):
        return self.name

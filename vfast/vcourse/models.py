#!encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from vuser.models import User


# Create your models here.
class Technology(models.Model):
    name = models.CharField('技术类别', max_length=50)
    color = models.CharField('颜色', max_length=50, default='#FFFFFF')
    desc = models.TextField('技术简介', default='')

    def __unicode__(self):
        return self.name


class Course(models.Model):
    PUB_STATUS = (
        (0, '已发布'),
        (1, '即将发布'),
    )
    ICON_STATUS = (
        (0, '视频'),
        (1, '项目')
    )

    name = models.CharField('课程名称', max_length=50)
    desc = models.TextField('课程描述', null=True, blank=True, default='')
    totaltime = models.CharField('课程总时长', max_length=50, null=True, blank=True, default='')
    difficult = models.IntegerField('课程难度', null=True, blank=True, default=4)
    tech = models.ForeignKey(Technology, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='技术分类')
    icon = models.IntegerField('课程对应的图标', choices=ICON_STATUS, default=0)
    color = models.CharField('颜色', max_length=30, null=True, blank=True)
    pubstatus = models.IntegerField('发布状态', choices=PUB_STATUS, null=True, default=1)
    subscibe = models.IntegerField('学习课程人数', null=True, blank=True, default=0)
    createtime = models.DateField('课程创建时间', auto_now=True)
    teach = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者1',
                              limit_choices_to={'id': 2})
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='teacher', null=True, blank=True,
                                verbose_name='作者2', limit_choices_to={'id': 2})
    pubdate = models.CharField('课程发布时间', max_length=50, default='即将发布', blank=True)
    tag = models.CharField('标签', max_length=50, default='')
    intrv = models.FileField('课程介绍视频', upload_to='course/video', default='course/video/1.mp4')
    target_user = models.TextField('目标受众', default='')
    require_knowledge = models.TextField('先修要求', default='')
    require_env = models.TextField('软硬件要求', default='')

    def __unicode__(self):
        return self.name


class Section(models.Model):
    title = models.CharField('章节标题', max_length=100, default='')
    desc = models.TextField('章节描述', default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='所属课程')

    def __unicode__(self):
        return self.title


class Path(models.Model):
    name = models.CharField('路线名称', max_length=50)
    desc = models.TextField('路线简介', max_length=1000, blank=True, null=True, default='')
    intrv = models.FileField('路线介绍视频', upload_to='path/video')
    jobscount = models.CharField('岗位数', null=True, blank=True, default='', max_length=20)
    salary = models.CharField('岗位起薪', null=True, blank=True, max_length=50, default='10K')
    jstime = models.CharField('岗位&起薪统计时间', null=True, blank=True, max_length=50)
    difficult = models.IntegerField('路径难度', null=True, blank=True, default=5)
    pathimg = models.ImageField('路线图片', upload_to='path/img')
    pathwel = models.ImageField('路线介绍页面图面', upload_to='path/img')
    totaltime = models.CharField('路线总时长', null=True, blank=True, default='', max_length=50)
    subscibe = models.IntegerField('参加路线人数', null=True, blank=True)
    createtime = models.DateField('路线创建时间', auto_now=True)
    p_sequence = models.CharField('课程顺序', null=True, blank=True, max_length=30)
    color = models.CharField('路线颜色', null=True, blank=True, max_length=30, default='red')
    avrage_salary = models.CharField('平均入门薪水', max_length=10, null=True, blank=True, default='9000')
    job_wanted = models.IntegerField('岗位空缺度', null=True, default=5)

    def __unicode__(self):
        return self.name


class Video(models.Model):
    VTYPE = (
        (0, '视频'),
        (1, '题目'),
    )
    END_TYPE = (
        (0, '是'),
        (1, '不是'),
    )
    name = models.CharField('视频名称', max_length=100)
    vtime = models.CharField('视频时长', max_length=10, default='')
    vurl = models.FileField('视频存放位置', upload_to='video/%y%m%d', null=True, blank=True)
    cc = models.FileField('字幕存放位置', upload_to='video/%y%m%d', null=True, blank=True)
    notes = models.TextField('讲师笔记', default='', null=True, blank=True)
    score = models.IntegerField('总评星', null=True, blank=True, default=0)
    scorepeople = models.IntegerField('评星人数', null=True, blank=True, default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程ID')
    watched = models.IntegerField('观看视频人数', null=True, blank=True, default=0)
    createtime = models.DateField('视频上传时间', auto_now=True)
    end = models.IntegerField('是否为最后一节视频', choices=END_TYPE, default=0)  # 0是最后一个, 1不是最后一个
    vtype = models.IntegerField('视频, 题目', choices=VTYPE, default=0)
    sequence = models.IntegerField('视频播放顺序', unique=True, default=1)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='所属章节', null=True)

    def __unicode__(self):
        return self.name


class UserPath(models.Model):
    createtime = models.CharField('用户加入学习路线时间', max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    path = models.ForeignKey(Path, on_delete=models.CASCADE, verbose_name='路线ID')

    def __unicode__(self):
        return '%s,%s' % (self.user.username, self.path.name)

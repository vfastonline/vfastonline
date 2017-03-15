#!encoding:utf-8
from __future__ import unicode_literals
from vcourse.models import Video
from django.db import models
from vuser.models import User


# Create your models here.
class Timu(models.Model):
    sequence = models.IntegerField(null=True, blank=True, default=1, verbose_name='问题排序')
    title = models.CharField('题目标题', max_length=255, null=False)
    answer = models.CharField('正确答案', max_length=6)
    tips = models.CharField('错误提示', max_length=50)
    A = models.CharField('选项A', max_length=60, null=True, blank=True)
    B = models.CharField('选项B', max_length=60, null=True, blank=True)
    C = models.CharField('选项C', max_length=60, null=True, blank=True)
    D = models.CharField('选项D', max_length=60, null=True, blank=True)
    E = models.CharField('选项E', max_length=60, null=True, blank=True)
    F = models.CharField('选项F', max_length=60, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='视频ID')
    end = models.IntegerField('是否最后一个', default=1)   #0是最后一个, 1不是最后一个

    def __unicode__(self):
        return self.title


class Question(models.Model):
    title = models.CharField('问题标题', max_length=50)
    desc = models.TextField('问题描述')
    video = models.ForeignKey(Video, verbose_name='视频ID')
    createtime = models.CharField('问题发布时间', max_length=20)
    user = models.ForeignKey(User, verbose_name='用户ID')
    like = models.IntegerField('点赞')
    email_status = models.IntegerField('是否发送邮件', default=0)   #0发送邮件, 1不发送邮件

    def __unicode__(self):
        return self.title


class Replay(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题ID')
    replay_user = models.ForeignKey(User, verbose_name='回复人')
    createtime = models.CharField('回复时间', max_length=20)
    content = models.TextField('回复内容')
    like = models.IntegerField('点赞数')

    def __unicode__(self):
        return self.question.title
#!encoding:utf-8
from __future__ import unicode_literals
from vcourse.models import Video
from django.db import models
from vuser.models import User


# Create your models here.
class Timu(models.Model):
    sequence = models.IntegerField(null=True, blank=True, default=1, verbose_name='问题排序')
    title = models.CharField('问题描述', max_length=255, null=False)
    answer = models.CharField('正确答案', max_length=6)
    tips = models.CharField('错误提示', max_length=50)
    A = models.CharField('选项A', max_length=60, null=True, blank=True)
    B = models.CharField('选项B', max_length=60, null=True, blank=True)
    C = models.CharField('选项C', max_length=60, null=True, blank=True)
    D = models.CharField('选项D', max_length=60, null=True, blank=True)
    E = models.CharField('选项E', max_length=60, null=True, blank=True)
    F = models.CharField('选项F', max_length=60, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='视频ID', limit_choices_to={'vtype':1})

    def __unicode__(self):
        return self.title


class Question(models.Model):
    title = models.CharField('问题标题', max_length=50)
    desc = models.TextField('问题描述')
    video = models.ForeignKey(Video, verbose_name='视频ID')
    createtime = models.CharField('问题发布时间', max_length=20)
    user = models.ForeignKey(User, verbose_name='用户ID')
    like = models.IntegerField('点赞数', default=0)
    dislike = models.IntegerField('不赞数', default=0)
    email_status = models.IntegerField('是否发送邮件', default=0)   #0发送邮件, 1不发送邮件
    score = models.IntegerField('分数', default=0)        #点赞+1分, 踩-1分
    status = models.IntegerField('问题状态', default=0)   #0为未解决状态, 1为解决状态
    add_repatation = models.IntegerField('悬赏声望', default=0)
    add_repatation_user = models.IntegerField('悬赏人的ID', null=True, blank=True)
    default_repatation = models.IntegerField('默认声望', default=5)


    def __unicode__(self):
        return self.title


class Replay(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题ID')
    replay_user = models.ForeignKey(User, verbose_name='回复人')
    createtime = models.CharField('回复时间', max_length=20)
    content = models.TextField('回复内容')
    like = models.IntegerField('点赞数', default=0)
    dislike = models.IntegerField('不赞数', default=0)
    score = models.IntegerField('分数', default=0)        #点赞+1分, 踩-1分
    best = models.IntegerField('是否最佳', default=0)      #0不是最佳, 1为最佳答案

    def __unicode__(self):
        return self.question.title


class QRcomment(models.Model):
    qid = models.IntegerField('问题ID', null=True)
    rid = models.IntegerField('回复ID', null=True)
    uid = models.IntegerField('用户ID')
    type = models.CharField('问题或回复, 是否点赞', max_length=1)    #(Q, R)
    status = models.IntegerField('赞,踩', default=0)   #(1, 赞, -1, 猜)

    def __unicode__(self):
        return '%s, %s' % (self.qid, self.uid)


class Attention(models.Model):
    qid = models.IntegerField('问题ID')
    uid = models.IntegerField('用户ID')

    def __unicode__(self):
        return '%s, %s' % (self.qid, self.uid)


class Repatation(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    tech_id = models.IntegerField('技术类别ID', null=True)
    createtime = models.CharField('创建时间', max_length=22)
    repa_grade = models.IntegerField('所得声望')
    repatype = models.IntegerField('获取声望途径', default=1)

    def __unicode__(self):
        return '%s, %s' % (self.user.nickname, self.rep)


class RepaType(models.Model):
    name = models.CharField('声望获取途径', max_length=50)

    def __unicode__(self):
        return self.name
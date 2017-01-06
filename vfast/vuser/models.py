#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        (0, '女'),
        (1, '男')
    )
    IS_OPEN = (
        (0, '公开'),
        (1, '不公开')
    )

    username = models.CharField('用户名称', max_length=50, null=True, blank=True, default=' ')
    realname = models.CharField('用户真实姓名', max_length=30, null=True, blank=True, default=' ')
    email = models.EmailField('邮箱', max_length=50)
    password = models.CharField('密码', max_length=100)
    sex = models.IntegerField('性别', choices=SEX)
    totalscore = models.IntegerField('用户总得分', null=True, blank=True, default=0)
    location = models.CharField('所在城市', max_length=50, null=True, blank=True, default=' ')
    intro = models.CharField('个人简介', max_length=500, null=True, blank=True, default=' ')
    is_open = models.IntegerField('个人信息是否展示', choices=IS_OPEN, default=0)
    birthday = models.DateField('出生日期', null=True, blank=True)
    program_exp = models.CharField('计算机编程经验', max_length=50, null=True, blank=True, default=' ')
    into_it = models.CharField('是否从事IT行业', max_length=10, null=True, blank=True, default=' ')
    comp_use_time_day = models.CharField('使用电脑频率', max_length=50, null=True, blank=True, default=' ')
    githuburl = models.CharField('github主页', max_length=50, null=True, blank=True, default=' ')
    linkinurl = models.CharField('linkin主页', max_length=50, null=True, blank=True, default=' ')
    stackoverflowurl = models.CharField('stackoverflow主页', max_length=50, null=True, blank=True, default=' ')
    personpage = models.CharField('个人主页', max_length=50, null=True, blank=True, default=' ')
    expect_job = models.CharField('期望工作', max_length=100, null=True, blank=True, default=' ')
    expect_level = models.CharField('期望级别', max_length=50, null=True, blank=True, default=' ')
    current_company = models.CharField('当前所在公司', max_length=100, null=True, blank=True, default=' ')
    company_location = models.CharField('公司所在地', max_length=100, null=True, blank=True, default=' ')
    mugshot = models.CharField('头像URL', max_length=100, null=True, blank=True, default=' ')
    mugshotframe = models.CharField('画框URL', max_length=100, null=True, blank=True, default=' ')
    createtime = models.BigIntegerField('创建时间', null=True, blank=True, default=0)
    # pathid = models.ForeignKey(Path)

    def __unicode__(self):
        return self.email


class Badge(models.Model):
    badgename = models.CharField('勋章名称', max_length=100, null=True, blank=True, default=' ')
    badgeurl = models.CharField('勋章图片位置', max_length=100, null=True, blank=True, default=' ')
    createtime = models.BigIntegerField('勋章创建时间', null=True, blank=True, default=0)
    # cid = models.ForeignKey(Course)

    def __unicode__(self):
        return self.badgename


class UserBadge(models.Model):
    userid = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='用户ID')
    badgeid = models.ForeignKey(Badge, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='勋章ID')
    gain_time = models.BigIntegerField('勋章获取时间', null=True, blank=True, default=0)
#!encoding: utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Headimg(models.Model):
    name = models.CharField('头像名称', max_length=100, null=True, blank=True, default=' ')
    url = models.CharField('头像图片位置', max_length=100, null=True, blank=True, default=' ')
    createtime = models.CharField('创建时间', max_length=20)
    type = models.IntegerField('头像类型', default=1)     #系统默认头像为1, 用户自定义上传的为2

    def __unicode__(self):
        return self.name

class Headframe(models.Model):
    name = models.CharField('画框名称', max_length=100)
    url = models.CharField('画框图片位置', max_length=100)
    createtime = models.CharField('创建时间', max_length=20)

    def __unicode__(self):
        return self.name

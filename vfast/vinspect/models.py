#!encoding: utf-8
from __future__ import unicode_literals

from django.db import models

from vuser.models import User


class Inspect(models.Model):
    name = models.CharField(verbose_name='问卷名称', max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "问卷"


class InspectOption(models.Model):
    inspect = models.ForeignKey(Inspect, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='名字', max_length=200)
    A = models.CharField(verbose_name='选项A', max_length=100)
    B = models.CharField(verbose_name='选项B', max_length=100)
    C = models.CharField(verbose_name='选项C', max_length=100)
    D = models.CharField(verbose_name='选项D', max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "问卷选项"


class InspectResult(models.Model):
    inspect = models.ForeignKey(Inspect, on_delete=models.CASCADE)
    inspectoption = models.ForeignKey(InspectOption, verbose_name='选项', null=True)
    option = models.CharField(verbose_name='选项', max_length=2, null=True)
    user = models.ForeignKey(User, verbose_name='用户', null=True)
    opinion = models.TextField(verbose_name='意见', default='')

    def __unicode__(self):
        return self.inspect.name

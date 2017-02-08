#!encoding: utf-8
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Role(models.Model):
    rolename = models.CharField('身份名称', max_length=20, null=False)

    def __unicode__(self):
        return self.rolename


class Perm(models.Model):
    pass


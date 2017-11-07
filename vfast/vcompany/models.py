#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models

from vuser.models import User


class Company(models.Model):
    AUDIT_STATUS = (
        (0, '未通过'),
        (1, '已通过'),
    )
    createtime = models.CharField('创建时间', max_length=20, blank=True)
    fullname = models.CharField('公司全称', max_length=100)
    name = models.CharField('公司简称', max_length=50)
    trade = models.CharField('公司行业', max_length=20, null=True, blank=True)
    scale = models.CharField('公司人员规模', max_length=20, null=True, blank=True)
    intro = models.TextField('公司团队亮点', null=True, blank=True)
    forwho = models.CharField('自主招聘or猎头招聘', max_length=10, null=True, blank=True)
    period = models.CharField('招聘周期', max_length=20, null=True, blank=True)
    technology_type = models.CharField('招聘技术类别, java, python', max_length=100, null=True, blank=True)
    wanted_exp = models.CharField('实习生,工作经验的', max_length=50, null=True, blank=True)
    work_address = models.CharField('工作所在地', max_length=20, null=True, blank=True)
    logo = models.CharField('公司logo', max_length=100, null=True, blank=True)
    homepage = models.CharField('公司官网', max_length=100, null=True, blank=True)
    finacing = models.CharField('融资阶段', max_length=20, null=True, blank=True)
    business_license = models.CharField('营业执照', max_length=100, null=True, blank=True)
    audit_status = models.IntegerField('是否通过审核', default=0)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='管理者的ID')

    def __unicode__(self):
        return self.fullname

    class Meta:
        verbose_name = "公司"

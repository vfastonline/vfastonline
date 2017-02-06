#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Role(models.Model):
    rolename = models.CharField('身份名称', max_length=20, null=False)

    def __unicode__(self):
        return self.rolename


class User(models.Model):
    SEX = (
        (0, '女'),
        (1, '男'),
        (2, '保密')
    )
    IS_OPEN = (
        (0, '公开'),
        (1, '不公开')
    )
    STATUS = (
        (0, '未激活'),
        (1, '激活')
    )
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    username = models.CharField('用户名称', max_length=50, null=True, blank=True, default=' ')
    realname = models.CharField('用户真实姓名', max_length=30, null=True, blank=True, default=' ')
    email = models.EmailField('邮箱', max_length=50)
    password = models.CharField('密码', max_length=100)
    sex = models.IntegerField('性别', choices=SEX, default=3)
    totalscore = models.IntegerField('用户总得分', null=True, blank=True, default=0)
    location = models.CharField('所在城市', max_length=50, null=True, blank=True, default=' ')
    intro = models.CharField('个人简介', max_length=500, null=True, blank=True, default=' ')
    is_open = models.IntegerField('个人信息是否展示', choices=IS_OPEN, default=0)
    birthday = models.DateField('出生日期', null=True, blank=True)
    program_exp = models.CharField('计算机编程经验', max_length=50, null=True, blank=True, default=' ')
    into_it = models.CharField('是否从事IT行业', max_length=10, null=True, blank=True, default=' ')
    comp_use_time_day = models.CharField('使用电脑频率', max_length=50, null=True, blank=True, default=' ')
    learn_habit = models.CharField('学习习惯', max_length=50, null=True, blank=True, default=' ')
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
    createtime = models.DateTimeField('创建时间')
    active = models.CharField('激活账号码', max_length=100, null=True, blank=True)
    status = models.IntegerField('是否激活', default=0)
    pathid = models.IntegerField('正在进行的路径ID', default=0)
    phone = models.CharField('公司电话号码', max_length=20, null=True, blank=True, default=' ')
    gongpai = models.CharField('工牌图片', max_length=100, null=True, blank=True, default=' ')
    on_job_verify = models.CharField('在职证明', max_length=100, null=True, blank=True, default='')
    joblevel = models.CharField('岗位职称', max_length=20, null=True, blank=True, default=True)

    def __unicode__(self):
        return self.email


class Company(models.Model):
    AUDIT_STATUS = (
        (0, '未通过'),
        (1, '已通过'),
    )
    fullname = models.CharField('公司全称', max_length=100)
    name = models.CharField('公司简称', max_length=50, null=True)
    trade = models.CharField('公司行业', max_length=20, null=True)
    scale = models.CharField('公司人员规模', max_length=20, null=True)
    intro = models.TextField('公司团队亮点', null=True)
    forwho = models.CharField('自主招聘or猎头招聘', max_length=10, null=True)
    period = models.CharField('招聘周期', max_length=20, null=True)
    technology_type = models.CharField('招聘技术类别, java, python', max_length=100, null=True)
    wanted_exp = models.CharField('实习生,工作经验的', max_length=50, null=True)
    work_address = models.CharField('工作所在地', max_length=20, null=True)
    logo = models.CharField('公司logo', max_length=100, null=True)
    homepage = models.CharField('公司官网', max_length=100, null=True)
    finacing = models.CharField('融资阶段', max_length=20, null=True)
    business_license = models.CharField('营业执照', max_length=100, null=True)
    audit_status = models.IntegerField('是否通过审核', default=0)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='管理者的ID')

    def __unicode__(self):
        return self.fullname

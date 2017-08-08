#!encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from vperm.models import Role


# Create your models here.

class User(models.Model):
    IS_OPEN = (
        (0, '公开'),
        (1, '不公开')
    )
    STATUS = (
        (0, '未激活'),
        (1, '激活')
    )
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    realname = models.CharField('用户真实姓名', max_length=30, null=True, blank=True, default='')
    email = models.EmailField('邮箱', max_length=50, null=True, unique=True)
    password = models.CharField('密码', max_length=100, null=True)
    sex = models.CharField('性别', max_length=4, default='')
    totalscore = models.IntegerField('用户总得分', null=True, blank=True, default=10)
    city = models.CharField('所在城市', max_length=50, null=True, blank=True, default='')
    intro = models.TextField('个人简介', null=True, blank=True, default='')
    is_open = models.IntegerField('个人信息是否展示', choices=IS_OPEN, default=0, null=True)
    birthday = models.CharField('出生日期', max_length=20, null=True, blank=True, default='')
    program_exp = models.CharField('计算机编程经验', max_length=50, null=True, blank=True, default='')
    into_it = models.CharField('是否从事IT行业', max_length=10, null=True, blank=True, default='')
    comp_use_time_day = models.CharField('使用电脑频率', max_length=50, null=True, blank=True, default='')
    learn_habit = models.CharField('学习习惯', max_length=50, null=True, blank=True, default='')
    githuburl = models.CharField('github主页', max_length=50, null=True, blank=True, default='')
    githubrepo = models.CharField('github 项目', max_length=50, null=True, blank=True, default='')
    personpage = models.CharField('个人主页', max_length=50, null=True, blank=True, default='')
    expect_job = models.CharField('期望工作', max_length=100, null=True, blank=True, default='')
    expect_level = models.CharField('期望级别', max_length=50, null=True, blank=True, default='')
    current_company = models.CharField('当前所在公司', max_length=100, null=True, blank=True, default='')
    company_gangwei = models.CharField('岗位', max_length=100, null=True, blank=True, default='')
    headimg = models.CharField('头像URL', max_length=100, null=True, blank=True, default='')
    createtime = models.CharField('创建时间', max_length=20)
    active = models.CharField('激活账号码', max_length=250, null=True, blank=True)
    status = models.IntegerField('是否激活', default=0)
    pathid = models.IntegerField('正在进行的路径ID', default=0)
    position = models.CharField('讲师职位', default='讲师', max_length=100)
    phone = models.CharField('手机号码', max_length=15, unique=True)
    nickname = models.CharField('昵称', max_length=30, unique=True)

    #HR注册的相关信息
    hr_phone = models.CharField('公司电话号码', max_length=20, null=True, blank=True, default='')
    idcard = models.CharField('身份证图片', max_length=200, null=True, blank=True, default='')
    gongpai = models.CharField('工牌图片', max_length=100, null=True, blank=True, default='')
    on_job_verify = models.CharField('在职证明', max_length=100, null=True, blank=True, default='')
    joblevel = models.CharField('岗位职称', max_length=20, null=True, blank=True, default='')
    companyid = models.IntegerField('关联公司', null=True, blank=True)

    def __unicode__(self):
        return self.nickname


class DailyTask(models.Model):
    user_id = models.IntegerField('用户ID')
    createtime = models.CharField('创建时间', max_length=20, default='')
    video_id = models.IntegerField('视频ID')
    vtype = models.IntegerField('视频类型', default=0)
    vtime = models.CharField('视频时长', max_length=20, default='')
    video_name = models.CharField('视频名称', max_length=50, default='')

    def __unicode__(self):
        return self.video_name


class PtoP(models.Model):
    follow = models.ForeignKey(User, verbose_name='关注人', related_name='follow')
    followed = models.ForeignKey(User, verbose_name='被关注的人', related_name='followed')

    def __unicode__(self):
        return self.follow.nickname


class Headimg(models.Model):
    url = models.ImageField('头像', upload_to='user/headimg')
    createtime = models.DateTimeField('创建时间', auto_now=True)

    def __unicode__(self):
        return self.name



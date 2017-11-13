#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from vuser.models import User


class Resume(models.Model):
    """个人简历基础信息"""
    user_id = models.ForeignKey(User, verbose_name=u"用户信息", related_name="resume_user_id", unique=True)
    years_of_service = models.IntegerField(u"工作年限", null=True, blank=True, default=0)
    education = models.CharField(u"最高学历", max_length=255, null=True, blank=True, default="")
    expect_salary_low = models.CharField(u"期望薪资最低", max_length=255, null=True, blank=True, default="")
    expect_salary_high = models.CharField(u"期望薪资最高", max_length=255, null=True, blank=True, default="")
    work_status = models.CharField(u"在职状态", max_length=255, null=True, blank=True, default="")
    company = models.CharField(u"现任公司", max_length=255, null=True, blank=True, default="")
    position = models.CharField(u"现任职务", max_length=255, null=True, blank=True, default="")
    my_advantage = models.TextField(u"我的优势", null=True, blank=True, default="")

    def __str__(self):
        return self.user_id.nickname

    class Meta:
        verbose_name = u"个人简历基础信息"
        verbose_name_plural = u"个人简历基础信息"
        index_together = ["user_id"]


class CareerObjective(models.Model):
    """求职意向"""
    user_id = models.ForeignKey(User, verbose_name=u"用户信息", related_name="careerobjective_user_id")
    position = models.CharField(u"期望职位", max_length=255, null=True, blank=True, default="")
    expect_salary_low = models.CharField(u"期望薪资最低", max_length=255, null=True, blank=True, default="")
    expect_salary_high = models.CharField(u"期望薪资最高", max_length=255, null=True, blank=True, default="")
    city = models.CharField(u"期望城市", max_length=255, null=True, blank=True, default="")
    industry = models.CharField(u"期望行业", max_length=255, null=True, blank=True, default="")

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = u"求职意向"
        verbose_name_plural = u"求职意向"
        ordering = ['-id']
        index_together = ["user_id"]


class WorkExperience(models.Model):
    """工作经历"""
    user_id = models.ForeignKey(User, verbose_name=u"用户信息", related_name="workexperience_user_id")
    company = models.CharField(u"公司名称", max_length=255, null=True, blank=True, default="")
    position = models.CharField(u"职位名称", max_length=255, null=True, blank=True, default="")
    start_time = models.CharField(u"在职起始时间", max_length=255, null=True, blank=True, default="")
    end_time = models.CharField(u"在职终止时间", max_length=255, null=True, blank=True, default="")
    content = models.TextField(u"工作内容", null=True, blank=True, default="")

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = u"工作经历"
        verbose_name_plural = u"工作经历"
        ordering = ['-id']
        index_together = ["user_id"]


class ProjectExperience(models.Model):
    """项目经验"""
    user_id = models.ForeignKey(User, verbose_name=u"用户信息", related_name="projectexperience_user_id")
    project_name = models.CharField(u"项目名称", max_length=255, null=True, blank=True, default="")
    role = models.CharField(u"角色", max_length=255, null=True, blank=True, default="")
    url = models.CharField(u"项目链接", max_length=255, null=True, blank=True, default="")
    start_time = models.CharField(u"项目起始时间", max_length=255, null=True, blank=True, default="")
    end_time = models.CharField(u"项目终止时间", max_length=255, null=True, blank=True, default="")
    description = models.TextField(u"项目描述", null=True, blank=True, default="")

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = u"项目经验"
        verbose_name_plural = u"项目经验"
        ordering = ['-id']
        index_together = ["user_id"]


class EducationExperience(models.Model):
    """教育经历"""
    user_id = models.ForeignKey(User, verbose_name=u"用户信息", related_name="educationexperience_user_id")
    school = models.CharField(u"学校名称", max_length=255, null=True, blank=True, default="")
    discipline = models.CharField(u"所学专业", max_length=255, null=True, blank=True, default="")
    education = models.CharField(u"学历", max_length=255, null=True, blank=True, default="")
    start_time = models.CharField(u"起始时间", max_length=255, null=True, blank=True, default="")
    end_time = models.CharField(u"终止时间", max_length=255, null=True, blank=True, default="")
    experience_at_school = models.TextField(u"在校经历", null=True, blank=True, default="")

    def __str__(self):
        return self.school

    class Meta:
        verbose_name = u"教育经历"
        verbose_name_plural = u"教育经历"
        ordering = ['-id']
        index_together = ["user_id"]

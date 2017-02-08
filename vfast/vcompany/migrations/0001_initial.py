# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-08 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createtime', models.CharField(blank=True, max_length=20, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('fullname', models.CharField(max_length=100, verbose_name='\u516c\u53f8\u5168\u79f0')),
                ('name', models.CharField(max_length=50, verbose_name='\u516c\u53f8\u7b80\u79f0')),
                ('trade', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u516c\u53f8\u884c\u4e1a')),
                ('scale', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u516c\u53f8\u4eba\u5458\u89c4\u6a21')),
                ('intro', models.TextField(blank=True, null=True, verbose_name='\u516c\u53f8\u56e2\u961f\u4eae\u70b9')),
                ('forwho', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u81ea\u4e3b\u62db\u8058or\u730e\u5934\u62db\u8058')),
                ('period', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u62db\u8058\u5468\u671f')),
                ('technology_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u62db\u8058\u6280\u672f\u7c7b\u522b, java, python')),
                ('wanted_exp', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5b9e\u4e60\u751f,\u5de5\u4f5c\u7ecf\u9a8c\u7684')),
                ('work_address', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u5de5\u4f5c\u6240\u5728\u5730')),
                ('logo', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u516c\u53f8logo')),
                ('homepage', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u516c\u53f8\u5b98\u7f51')),
                ('finacing', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u878d\u8d44\u9636\u6bb5')),
                ('business_license', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u8425\u4e1a\u6267\u7167')),
                ('audit_status', models.IntegerField(default=0, verbose_name='\u662f\u5426\u901a\u8fc7\u5ba1\u6838')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vuser.User', verbose_name='\u7ba1\u7406\u8005\u7684ID')),
            ],
        ),
    ]

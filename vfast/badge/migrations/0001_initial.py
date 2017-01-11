# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-11 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vuser', '0001_initial'),
        ('vcourse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badgename', models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='\u52cb\u7ae0\u540d\u79f0')),
                ('badgeurl', models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='\u52cb\u7ae0\u56fe\u7247\u4f4d\u7f6e')),
                ('createtime', models.DateTimeField(verbose_name='\u52cb\u7ae0\u521b\u5efa\u65f6\u95f4')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vcourse.Course')),
            ],
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gain_time', models.DateTimeField(verbose_name='\u52cb\u7ae0\u83b7\u53d6\u65f6\u95f4')),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='badge.Badge', verbose_name='\u52cb\u7ae0ID')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vuser.User', verbose_name='\u7528\u6237ID')),
            ],
        ),
    ]

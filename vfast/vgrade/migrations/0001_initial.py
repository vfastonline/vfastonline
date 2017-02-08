# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-08 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Headframe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u753b\u6846\u540d\u79f0')),
                ('url', models.CharField(max_length=100, verbose_name='\u753b\u6846\u56fe\u7247\u4f4d\u7f6e')),
                ('createtime', models.CharField(max_length=20, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='Headimg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='\u5934\u50cf\u540d\u79f0')),
                ('url', models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='\u5934\u50cf\u56fe\u7247\u4f4d\u7f6e')),
                ('createtime', models.CharField(max_length=20, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('type', models.IntegerField(default=1, verbose_name='\u5934\u50cf\u7c7b\u578b')),
            ],
        ),
    ]

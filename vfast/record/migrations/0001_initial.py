# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-11 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vcourse', '0001_initial'),
        ('vuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createtime', models.DateField(verbose_name='\u83b7\u5f97\u79ef\u5206\u7684\u65e5\u671f')),
                ('score', models.IntegerField(verbose_name='\u83b7\u5f97\u79ef\u5206')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vcourse.Course', verbose_name='\u8bfe\u7a0bID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vuser.User', verbose_name='\u7528\u6237ID')),
            ],
        ),
        migrations.CreateModel(
            name='WatchRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_progress', models.IntegerField(verbose_name='\u89c2\u770b\u65f6\u95f4\u8fdb\u5ea6')),
                ('status', models.IntegerField(choices=[(0, '\u5df2\u770b\u5b8c'), (1, '\u672a\u770b\u5b8c')], verbose_name='\u89c2\u770b\u72b6\u6001')),
                ('recordtime', models.DateTimeField(verbose_name='\u8bb0\u5f55\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vcourse.Course', verbose_name='\u8bfe\u7a0bID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vuser.User', verbose_name='\u7528\u6237ID')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vcourse.Video', verbose_name='\u89c6\u9891ID')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcourse', '0004_auto_20170109_0350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='appraise',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='location',
            new_name='video',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='subtitle',
            new_name='zimu',
        ),
        migrations.AddField(
            model_name='video',
            name='scorepeople',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='\u8bc4\u661f\u4eba\u6570'),
        ),
    ]

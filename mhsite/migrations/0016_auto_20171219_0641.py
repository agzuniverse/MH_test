# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 01:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhsite', '0015_merge_20171218_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='messcut',
            name='approved_dates',
            field=models.CharField(default=True, max_length=100000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messcut',
            name='last_modified',
            field=models.DateField(default=datetime.date(2017, 12, 19)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messcut',
            name='rejected_dates',
            field=models.CharField(default='False', max_length=100000),
            preserve_default=False,
        ),
    ]

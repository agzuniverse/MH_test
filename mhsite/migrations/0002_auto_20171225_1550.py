# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-25 10:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mhsite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='e_mail',
            new_name='email',
        ),
    ]

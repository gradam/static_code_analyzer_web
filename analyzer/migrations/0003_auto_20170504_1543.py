# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0002_auto_20170504_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='last_checked',
            new_name='last_analyzed',
        ),
    ]

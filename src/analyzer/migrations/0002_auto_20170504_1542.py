# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='last_checked',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SnoutPage', '0009_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.BooleanField(default=False),
        ),
    ]

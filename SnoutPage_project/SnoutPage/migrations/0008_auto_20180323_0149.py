# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-23 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SnoutPage', '0007_auto_20180323_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetest',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='imagetest',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
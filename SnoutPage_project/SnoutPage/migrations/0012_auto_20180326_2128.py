# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SnoutPage', '0011_auto_20180326_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='picture',
            field=models.FileField(blank=True, upload_to=b'pet_profile_images'),
        ),
    ]

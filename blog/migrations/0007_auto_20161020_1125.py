# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-20 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20161020_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]

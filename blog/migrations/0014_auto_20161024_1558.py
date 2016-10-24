# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 07:58
from __future__ import unicode_literals

import blog.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20161023_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, storage=blog.storage.OverwriteStorage, upload_to='profile_image'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-22 09:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20161022_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='collectors',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

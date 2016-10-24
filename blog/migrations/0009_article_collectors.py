# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-21 16:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_auto_20161021_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='collectors',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-26 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0015_auto_20160504_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(blank=True, upload_to='recipe_photos'),
        ),
    ]
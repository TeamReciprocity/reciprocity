# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_auto_20160501_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_auto_20160504_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ancestors',
            field=models.ManyToManyField(related_name='_recipe_ancestors_+', to='recipe.Recipe'),
        ),
    ]
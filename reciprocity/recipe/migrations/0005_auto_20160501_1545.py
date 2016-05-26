# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 22:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_recipe_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='recipe.Recipe'),
        ),
    ]

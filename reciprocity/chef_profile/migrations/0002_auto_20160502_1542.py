# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_auto_20160501_2116'),
        ('chef_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chefprofile',
            name='about_me',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chefprofile',
            name='disliked_ingredients',
            field=models.ManyToManyField(blank=True, related_name='disliked_by', to='recipe.Ingredient'),
        ),
        migrations.AddField(
            model_name='chefprofile',
            name='liked_ingredients',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to='recipe.Ingredient'),
        ),
        migrations.AlterField(
            model_name='chefprofile',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_of', to='recipe.Recipe'),
        ),
    ]

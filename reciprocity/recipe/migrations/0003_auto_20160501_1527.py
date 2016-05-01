# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_recipe_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True, help_text='Tell us about your recipe.', null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='directions',
            field=models.TextField(default='Chop it all and mix it up!', help_text='How is this recipe prepared?'),
            preserve_default=False,
        ),
    ]

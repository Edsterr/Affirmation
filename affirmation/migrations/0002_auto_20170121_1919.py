# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affirmation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='affirmation.UserProfile'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-14 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0007_auto_20160707_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='costo',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='costo',
            field=models.FloatField(default=0),
        ),
    ]
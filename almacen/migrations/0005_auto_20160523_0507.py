# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 05:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0004_auto_20160523_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='insumo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='almacen.Insumo'),
        ),
    ]

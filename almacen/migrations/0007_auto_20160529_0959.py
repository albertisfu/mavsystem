# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0006_entrada_salida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='insumo',
        ),
        migrations.AddField(
            model_name='insumo',
            name='stock',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='stock',
        ),
    ]

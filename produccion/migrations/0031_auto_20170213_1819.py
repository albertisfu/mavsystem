# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-14 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0030_costoespecialalmacen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cotizacion',
            name='costo',
        ),
        migrations.RemoveField(
            model_name='cotizacion',
            name='nota',
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='descripcion',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-15 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0012_costoespecial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='costoflete',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orden',
            name='direccionentrega',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='entrega',
            field=models.IntegerField(choices=[(1, 'Bodega'), (2, 'Flete')], default=1),
        ),
    ]
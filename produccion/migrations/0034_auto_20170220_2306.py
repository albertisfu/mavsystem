# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-21 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0033_auto_20170220_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='productocotizacion',
            name='costo',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='productoordenalmacen',
            name='costo',
            field=models.FloatField(default=0),
        ),
    ]

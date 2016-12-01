# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-01 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0017_cotizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='estatus',
            field=models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Confirmada'), (6, 'Entregada')], default=1),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-08 18:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0022_producto_costo_venta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='costo_venta',
            new_name='precio_venta',
        ),
    ]
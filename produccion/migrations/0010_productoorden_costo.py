# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-15 04:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0009_insumoproducto_costototal'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoorden',
            name='costo',
            field=models.FloatField(default=0),
        ),
    ]
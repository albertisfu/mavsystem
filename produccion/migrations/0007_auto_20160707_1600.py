# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 21:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0006_auto_20160626_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinsumoproducto',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
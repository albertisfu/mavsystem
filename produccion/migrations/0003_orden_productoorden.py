# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-26 07:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0002_producto_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=255)),
                ('fecha_expedicion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_entrega', models.DateTimeField()),
                ('estatus', models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Confirmada'), (3, 'Proceso'), (4, 'Conflicto'), (5, 'Cancelada')], default=1)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoOrden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('color', models.CharField(max_length=100)),
                ('unidad', models.IntegerField(choices=[(1, 'Pieza'), (2, 'Metro'), (3, 'Kilo'), (4, 'Litro')], default=1)),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Producto')),
            ],
        ),
    ]

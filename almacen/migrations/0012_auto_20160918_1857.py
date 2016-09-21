# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-18 23:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0013_auto_20160715_0235'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('almacen', '0011_auto_20160714_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('total', models.FloatField(default=0)),
                ('estatus', models.IntegerField(choices=[(1, 'Creada'), (2, 'Ingreso'), (3, 'Cancelada')], default=1)),
                ('iva', models.BooleanField(default=False)),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Orden')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenConcepto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidad', models.IntegerField(choices=[(1, 'Pieza'), (2, 'Metro'), (3, 'Kilo'), (4, 'Litro')], default=1)),
                ('cantidad', models.FloatField()),
                ('total', models.FloatField(default=0)),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produccion.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('id_unico', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('celular', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacen.Proveedor'),
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
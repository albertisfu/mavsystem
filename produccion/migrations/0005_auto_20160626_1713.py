# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produccion', '0004_auto_20160626_0258'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckInsumoProducto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('estatus', models.CharField(max_length=140)),
                ('insumo', models.ForeignKey(to='produccion.InsumoProducto')),
                ('productorden', models.ForeignKey(to='produccion.ProductoOrden')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comentariosorden',
            name='estatus',
            field=models.IntegerField(default=1, choices=[(1, 'Pendiente'), (2, 'Confirmada'), (3, 'Proceso'), (4, 'Conflicto'), (5, 'Cancelada')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productoorden',
            name='comentario',
            field=models.CharField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comentariosorden',
            name='comentario',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productoorden',
            name='color',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]

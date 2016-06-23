from __future__ import unicode_literals

from django.db import models

# Create your models here.
from almacen.models import Insumo

class Cliente(models.Model):
	nombrecontacto = models.CharField(max_length = 255)
	empresainstitucion = models.CharField(max_length = 500, blank=True, null=True)
	telefono = models.CharField(max_length = 100, blank=True, null=True)
	direccion = models.CharField(max_length = 500, blank=True, null=True)
	email = models.CharField(max_length = 500, blank=True, null=True)
	def __unicode__(self):
		return self.nombrecontacto

class Categoria(models.Model):
	nombre = models.CharField(max_length = 255)
	def __unicode__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length = 255)
	codigo = models.CharField(max_length = 100)
	descripcion = models.CharField(max_length = 255)
	categoria = models.ForeignKey(Categoria, blank=True, null=True)
	file = models.FileField(upload_to="static/files", verbose_name="Imagen", blank=True, null=True)
	def __unicode__(self):
		return self.nombre


class InsumoProducto(models.Model):
	insumo = models.ForeignKey(Insumo)
	producto = models.ForeignKey(Producto)
	cantidad = models.FloatField()
	def __unicode__(self):
		return self.insumo.nombre
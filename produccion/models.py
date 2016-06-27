from __future__ import unicode_literals

from django.db import models

# Create your models here.
from almacen.models import Insumo


from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User

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




class Orden(models.Model):
	nombre = models.CharField(max_length = 255)
	codigo = models.CharField(max_length = 100)
	descripcion = models.CharField(max_length = 255)
	cliente = models.ForeignKey(Cliente)
	fecha_expedicion = models.DateField(default=timezone.now)
	fecha_entrega = models.DateField()
	pendiente = 1
	confirmada = 2
	proceso = 3
	conflicto = 4
	cancelada = 5
	estatus_options = (
	      (pendiente, 'Pendiente'),
	      (confirmada, 'Confirmada'),
	      (proceso, 'Proceso'),
	      (conflicto, 'Conflicto'),
	      (cancelada, 'Cancelada'),
	  )
	estatus = models.IntegerField(choices=estatus_options, default=pendiente)
	usuario = models.ForeignKey(User, blank=True, null=True) #quitar null
	def __unicode__(self):
		return self.nombre


class ProductoOrden(models.Model):
	producto = models.ForeignKey(Producto)
	orden = models.ForeignKey(Orden)
	cantidad = models.FloatField()
	color = models.CharField(max_length = 100, blank=True, null=True)
	comentario = models.CharField(max_length = 1000, blank=True, null=True)
	pieza = 1
	metro = 2
	kilo = 3
	litro = 4
	unidad_options = (
	      (pieza, 'Pieza'),
	      (metro, 'Metro'),
	      (kilo, 'Kilo'),
	      (litro, 'Litro'),
	  )
	unidad = models.IntegerField(choices=unidad_options, default=pieza)
	def __unicode__(self):
		return self.producto.nombre

class ComentariosOrden(models.Model):
	orden = models.ForeignKey(Orden)
	fecha = models.DateTimeField(default=timezone.now)
	comentario = models.CharField(max_length = 500, blank=True, null=True)
	pendiente = 1
	confirmada = 2
	proceso = 3
	conflicto = 4
	cancelada = 5
	estatus_options = (
	      (pendiente, 'Pendiente'),
	      (confirmada, 'Confirmada'),
	      (proceso, 'Proceso'),
	      (conflicto, 'Conflicto'),
	      (cancelada, 'Cancelada'),
	  )
	estatus = models.IntegerField(choices=estatus_options, default=pendiente)
	usuario = models.ForeignKey(User)
	def __unicode__(self):
		return self.orden.nombre


class CheckInsumoProducto(models.Model):
	productorden = models.ForeignKey(ProductoOrden)
	insumo = models.ForeignKey(InsumoProducto)
	fecha = models.DateTimeField(default=timezone.now)
	estatus = models.CharField(max_length = 140)
	usuario = models.ForeignKey(User)
	def __unicode__(self):
		return self.orden.nombre


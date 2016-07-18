from __future__ import unicode_literals

from django.db import models

# Create your models here.
from almacen.models import Insumo


from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


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
	costo = models.FloatField(default=0)
	file = models.FileField(upload_to="static/files", verbose_name="Imagen", blank=True, null=True)
	def __unicode__(self):
		return self.nombre


class CostoEspecial(models.Model):
	producto = models.ForeignKey(Producto)
	concepto = models.CharField(max_length = 255)
	costo = models.FloatField(default=0)
	def __unicode__(self):
		return self.producto.nombre


class InsumoProducto(models.Model):
	insumo = models.ForeignKey(Insumo)
	producto = models.ForeignKey(Producto)
	cantidad = models.FloatField()
	costototal = models.FloatField(default=0)
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
	costo = models.FloatField(default=0)
	bodega = 1
	flete = 2
	entrega_options = (
	      (bodega, 'Bodega'),
	      (flete, 'Flete'),
	  )
	entrega = models.IntegerField(choices=entrega_options, default=bodega)
	direccionentrega = models.CharField(max_length = 255, blank=True, null=True)
	costoflete = models.FloatField(default=0)
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
	#costo = models.FloatField(default=0)
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
	usuario = models.ForeignKey(User, blank=True, null=True)
	def __unicode__(self):
		return self.productorden.producto.nombre



 #Crear Check insumos

@receiver(post_save, sender=ProductoOrden)  
def producto_orden(sender, instance, created,  **kwargs):
	currentinstanceid = instance.id
	productoorden = ProductoOrden.objects.get(pk=currentinstanceid)
	print productoorden
	#producto = Producto.objects.get(pk=productoorden.producto.pk)
	insumos = InsumoProducto.objects.filter(producto=productoorden.producto)
	print insumos
	for insumo in insumos:
		CheckInsumoProducto.objects.create(productorden=productoorden, insumo=insumo, estatus='Producto Creado' )

	productos = ProductoOrden.objects.filter(orden=productoorden.orden)
	costo=0
	for producto in productos:
		costo = costo+(producto.cantidad*producto.producto.costo)

	Orden.objects.filter(pk=productoorden.orden.id).update(costo=costo)

  
@receiver(post_save, sender=InsumoProducto)  
def producto_insumo(sender, instance, created,  **kwargs):
	producto = instance.producto
	materials = InsumoProducto.objects.filter(producto=producto)
	costoproducto = 0
	for material in materials:
		costotinsumo = material.insumo.costounitario * material.cantidad
		InsumoProducto.objects.filter(pk=material.id).update(costototal=costotinsumo)
		costoproducto = costoproducto + costotinsumo

	costoespeciales = CostoEspecial.objects.filter(producto=producto)
	costoespecial = 0
	for costoe in costoespeciales:
		costoespecial = costoespecial + costoe.costo

	costototalp = costoespecial + costoproducto
	Producto.objects.filter(pk=producto.id).update(costo=costototalp)


@receiver(post_save, sender=CostoEspecial)  
def producto_especial(sender, instance, created,  **kwargs):
	producto = instance.producto
	materials = InsumoProducto.objects.filter(producto=producto)
	costoproducto = 0
	for material in materials:
		costotinsumo = material.insumo.costounitario * material.cantidad
		InsumoProducto.objects.filter(pk=material.id).update(costototal=costotinsumo)
		costoproducto = costoproducto + costotinsumo

	costoespeciales = CostoEspecial.objects.filter(producto=producto)
	costoespecial = 0
	for costoe in costoespeciales:
		costoespecial = costoespecial + costoe.costo

	costototalp = costoespecial + costoproducto
	Producto.objects.filter(pk=producto.id).update(costo=costototalp)













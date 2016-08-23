from __future__ import unicode_literals

from django.db import models

from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Categoria(models.Model):
	nombre = models.CharField(max_length = 255)
	def __unicode__(self):
		return self.nombre


class Insumo(models.Model):
	nombre = models.CharField(max_length = 255)
	codigo = models.CharField(max_length = 140)
	descripcion = models.CharField(max_length = 255)
	categoria = models.ForeignKey(Categoria, blank=True, null=True)
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
	costounitario = models.FloatField(default=0)
	file = models.FileField(upload_to="static/files", verbose_name="Imagen")
	stock = models.FloatField(default=0)
	costostock = models.FloatField(default=0)

	def __unicode__(self):
		return self.nombre

"""
class Stock(models.Model):
	insumo = models.OneToOneField(Insumo)
	cantidad = models.IntegerField()
	def __unicode__(self):
		return self.insumo.nombre"""


class Entrada(models.Model):
	insumo = models.ForeignKey(Insumo)
	cantidad = models.FloatField()
	comentario = models.CharField(max_length = 1000)
	fecha = models.DateTimeField(default=timezone.now)
	usuario = models.ForeignKey(User) 
	def __unicode__(self):
		return self.insumo.nombre

class Salida(models.Model):
	insumo = models.ForeignKey(Insumo)
	cantidad = models.FloatField()
	comentario = models.CharField(max_length = 1000)
	fecha = models.DateTimeField(default=timezone.now)
	usuario = models.ForeignKey(User) 
	def __unicode__(self):
		return self.insumo.nombre

#signal suma stock
@receiver(post_save, sender=Entrada)  
def entrada_insumo(sender, instance, created,  **kwargs):
  currentinstanceid = instance.id
  entrada = Entrada.objects.get(pk=currentinstanceid)
  print entrada.cantidad
  insumo = Insumo.objects.get(pk=entrada.insumo.pk)
  print insumo
  print insumo.stock
  currentstock = insumo.stock
  print currentstock
  newstock = currentstock + entrada.cantidad
  print newstock
  costostock = insumo.costounitario * newstock
  Insumo.objects.filter(pk=entrada.insumo.pk).update(stock=newstock, costostock=costostock)

#signal resta stock
@receiver(post_save, sender=Salida)  
def salida_insumo(sender, instance, created,  **kwargs):
  currentinstanceid = instance.id
  salida = Salida.objects.get(pk=currentinstanceid)
  print salida.cantidad
  insumo = Insumo.objects.get(pk=salida.insumo.pk)
  print insumo
  print insumo.stock
  currentstock = insumo.stock
  print currentstock
  newstock = currentstock - salida.cantidad
  print newstock
  costostock = insumo.costounitario * newstock
  Insumo.objects.filter(pk=salida.insumo.pk).update(stock=newstock, costostock=costostock)
 
from produccion.models import InsumoProducto, Producto, CostoEspecial, ProductoOrden, Orden

@receiver(post_save, sender=Insumo)  
def nuevo_insumo(sender, instance, created,  **kwargs):
	currentinstanceid = instance.id
	insumo = Insumo.objects.get(pk=currentinstanceid)
	print insumo
	print insumo.stock
	currentstock = insumo.stock
	costostock = insumo.costounitario * currentstock
	Insumo.objects.filter(pk=currentinstanceid).update(costostock=costostock)
	#actualizar costo de insumoProducto cantidad de insumos para producto * costo unitario
	insumosp = InsumoProducto.objects.filter(insumo=insumo)
	
	for insumop in insumosp:
		costotinsumo = insumop.insumo.costounitario * insumop.cantidad
		InsumoProducto.objects.filter(pk=insumop.id).update(costototal=costotinsumo)
		productos = Producto.objects.filter(insumoproducto__id=insumop.id)
		for producto in productos:
			materials = InsumoProducto.objects.filter(producto=producto)
			costoproducto = 0
			for material in materials:
				costotinsumo = material.insumo.costounitario * material.cantidad
				#InsumoProducto.objects.filter(pk=material.id).update(costototal=costotinsumo)
				costoproducto = costoproducto + costotinsumo

			costoespeciales = CostoEspecial.objects.filter(producto=producto)
			costoespecial = 0
			for costoe in costoespeciales:
				costoespecial = costoespecial + costoe.costo

			costototalp = costoespecial + costoproducto
			Producto.objects.filter(pk=producto.id).update(costo=costototalp)

			productosorden = ProductoOrden.objects.filter(producto=producto)

			for productorder in productosorden:
				orders = Orden.objects.filter(productoorden__id=productorder.id)
				for order in orders:
					productos = ProductoOrden.objects.filter(orden=order)
					costo=0
					for producto in productos:
						costo = costo+(producto.cantidad*producto.producto.costo)

					Orden.objects.filter(pk=order.id).update(costo=costo)






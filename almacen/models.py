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
 



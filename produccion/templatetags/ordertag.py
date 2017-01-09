from django import template
from produccion.models import *
#from almacen.models import Insumo
from django.shortcuts import get_object_or_404
register = template.Library()


@register.simple_tag
def get_obj(insumo, orden):
	print insumo
	print orden
	producto_orden = get_object_or_404(ProductoOrden, pk = orden)
	insumo_producto =  get_object_or_404(InsumoProducto, pk = insumo)
	print producto_orden
	print insumo_producto
	obj = CheckInsumoProducto.objects.filter(insumo=insumo_producto, productorden=producto_orden).latest('fecha')
	estatus = obj.estatus
	print estatus
	return estatus


@register.simple_tag
def get_fecha(insumo, orden):
	producto_orden = get_object_or_404(ProductoOrden, pk = orden)
	insumo_producto =  get_object_or_404(InsumoProducto, pk = insumo)
	print producto_orden
	print insumo_producto
	obj = CheckInsumoProducto.objects.filter(insumo=insumo_producto, productorden=producto_orden).latest('fecha')
	fecha = obj.fecha
	print fecha
	return fecha


@register.simple_tag
def get_costo(cantidad, unitario):
	total = float(cantidad)*float(unitario)
	print total
	return total


@register.simple_tag
def get_obj_a(insumo, orden):
	print insumo
	print orden
	try:
		producto_orden = get_object_or_404(ProductoOrdenAlmacen, pk = orden)
	except:
		producto_orden = None
	try:
		insumo_producto =  get_object_or_404(InsumoProductoMod, pk = insumo)
	except:
		insumo_producto = None
	print producto_orden
	print insumo_producto
	try:
		obj = CheckInsumoProductoAlmacen.objects.filter(insumo=insumo_producto, productorden=producto_orden).latest('fecha')
	except:
		obj = None
		estatus = ''
	else:
		estatus = obj.estatus
	print estatus
	return estatus


@register.simple_tag
def get_fecha_a(insumo, orden):
	try:
		producto_orden = get_object_or_404(ProductoOrdenAlmacen, pk = orden)
	except:
		producto_orden = None
	try:
		insumo_producto =  get_object_or_404(InsumoProductoMod, pk = insumo)
	except:
		insumo_producto = None
	print producto_orden
	print insumo_producto
	try:
		obj = CheckInsumoProductoAlmacen.objects.filter(insumo=insumo_producto, productorden=producto_orden).latest('fecha')
	except:
		obj = None
		fecha = ''
	else:
		fecha = obj.fecha
	print fecha
	return fecha
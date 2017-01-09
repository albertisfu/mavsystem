# -*- coding: utf-8 -*-
from django import forms
from models import *


from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class altaProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = ('nombre', 'codigo', 'descripcion', 'precio_venta', 'categoria', 'file')
		labels = {
            'nombre': ('Nombre del producto'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripción'),
            'precio_venta': ('Precio Venta'),
        }


class ProductoInsumoForm(forms.ModelForm):
	class Meta:
		model = InsumoProducto
		fields = ('insumo', 'producto', 'cantidad')




class altaOrdenForm(forms.ModelForm):
	fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	fecha_entrega_almacen = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker1'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	class Meta:
		model = Orden
		fields = ('nombre', 'codigo', 'descripcion', 'cliente','fecha_entrega_almacen', 'usuario', 'entrega', 'direccionentrega', 'fecha_entrega', 'costoflete','nota')
		labels = {
            'nombre': ('Nombre de la orden'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
            'cliente': ('Seleccionar Cliente'),
            'fecha_entrega': ('Fecha de Entrega'),
            'fecha_entrega_almacen': ('Fecha de Entrega en almacen'),
            'entrega': ('Metodo de Entrega'),
            'direccionentrega': ('Dirección Entrega'),
            'costoflete': ('Costo Flete'),
            'nota': ('Nota'),
        }
		widgets = {
			'costoflete': forms.TextInput(),
		}



class altaOrdenAlmacenForm(forms.ModelForm):
	fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	fecha_entrega_almacen = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker1'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	class Meta:
		model = OrdenAlmacen
		fields = ('nombre', 'codigo', 'descripcion', 'cliente','fecha_entrega_almacen', 'usuario', 'entrega', 'direccionentrega', 'fecha_entrega', 'costoflete','nota')
		labels = {
            'nombre': ('Nombre de la orden'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
            'cliente': ('Seleccionar Cliente'),
            'fecha_entrega': ('Fecha de Entrega'),
            'fecha_entrega_almacen': ('Fecha de Entrega en almacen'),
            'entrega': ('Metodo de Entrega'),
            'direccionentrega': ('Dirección Entrega'),
            'costoflete': ('Costo Flete'),
            'nota': ('Nota'),
        }
		widgets = {
			'costoflete': forms.TextInput(),
		}


class altaCotizacionForm(forms.ModelForm):
	class Meta:
		model = Cotizacion
		fields = ('nombre', 'codigo', 'descripcion', 'cliente', 'usuario','nota')
		labels = {
            'nombre': ('Nombre de la cotización'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
            'cliente': ('Seleccionar Cliente'),
            'nota': ('Nota'),
        }
		widgets = {
			'costoflete': forms.TextInput(),
		}




class CostoEspecialForm(forms.ModelForm):
	class Meta:
		model = CostoEspecial
		fields = ('producto', 'concepto', 'costo')
		widgets = {
			'costo': forms.TextInput(),
		}
      



class comentarioOrdenForm(forms.ModelForm):
	class Meta:
		model = ComentariosOrden
		fields = ('orden', 'comentario', 'estatus', 'usuario')

class comentarioCotizacionForm(forms.ModelForm):
	class Meta:
		model = ComentariosCotizacion
		fields = ('orden', 'comentario', 'estatus', 'usuario')

class comentarioOrdenAlmacenForm(forms.ModelForm):
	class Meta:
		model = ComentariosOrden
		fields = ('orden', 'comentario', 'estatus', 'usuario')

class estatusProductoInsumo(forms.ModelForm):
	class Meta:
		model = CheckInsumoProducto
		fields = ('productorden', 'insumo', 'estatus', 'usuario')


class estatusProductoInsumoCotizacion(forms.ModelForm):
	class Meta:
		model = CheckInsumoProductoCotizacion
		fields = ('productorden', 'insumo', 'estatus', 'usuario')



#modal agregar categoria en producto nuevo
class productoaddcat(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ('nombre',)
		labels = {
			'nombre': ('Nombre de categoria'),
		}

#modal agregar nuevo cliente
class addcliente(forms.ModelForm):
	class Meta:
		model = Cliente
		fields = ('nombrecontacto','empresainstitucion','telefono','direccion','email')
		labels = {
			'nombrecontacto': ('Nombre de contacto'),
			'empresainstitucion': ('Empresa o institución'),
			'telefono': ('Telefono'),
			'direccion': ('Dirección'),
			'email': ('Email'),
		}
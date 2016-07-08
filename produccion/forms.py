# -*- coding: utf-8 -*-
from django import forms
from models import *


from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class altaProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = ('nombre', 'codigo', 'descripcion', 'categoria', 'file')
		labels = {
            'nombre': ('Nombre del producto'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
        }


class ProductoInsumoForm(forms.ModelForm):
	class Meta:
		model = InsumoProducto
		fields = ('insumo', 'producto', 'cantidad')




class altaOrdenForm(forms.ModelForm):
	fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	class Meta:
		model = Orden
		fields = ('nombre', 'codigo', 'descripcion', 'cliente', 'fecha_entrega', 'usuario')
		labels = {
            'nombre': ('Nombre de la orden'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
            'cliente': ('Seleccionar Cliente'),
            'fecha_entrega': ('Fecha de Entrega'),
        }


      



class comentarioOrdenForm(forms.ModelForm):
	class Meta:
		model = ComentariosOrden
		fields = ('orden', 'comentario', 'estatus', 'usuario')



class estatusProductoInsumo(forms.ModelForm):
	class Meta:
		model = CheckInsumoProducto
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
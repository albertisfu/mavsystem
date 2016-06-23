from django import forms
from models import *

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


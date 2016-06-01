from django import forms
from models import *

class AltaForm(forms.ModelForm):
	class Meta:
		model = Insumo
		fields = ('nombre', 'codigo', 'descripcion', 'categoria', 'unidad', 'file')
		labels = {
            'nombre': ('Nombre del insumo'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
        }




class EntradaForm(forms.ModelForm):
	class Meta:
		model = Entrada
		fields = ('cantidad', 'comentario', 'insumo', 'usuario', 'fecha')



class SalidaForm(forms.ModelForm):
	class Meta:
		model = Salida
		fields = ('cantidad', 'comentario', 'insumo', 'usuario', 'fecha')
# coding=utf-8


from django import forms
from models import *

class AltaForm(forms.ModelForm):
	class Meta:
		model = Insumo
		fields = ('nombre', 'codigo', 'descripcion', 'categoria', 'unidad', 'costounitario', 'file')
		labels = {
            'nombre': ('Nombre del insumo'),
            'codigo': ('Codigo Unico'),
            'descripcion': ('Descripcion'),
            'costounitario': ('Costo por unidad'),
        }
		widgets = {
			'costounitario': forms.TextInput(),
		}




class EntradaForm(forms.ModelForm):
	class Meta:
		model = Entrada
		fields = ('cantidad', 'comentario', 'insumo', 'usuario', 'fecha')



class SalidaForm(forms.ModelForm):
	class Meta:
		model = Salida
		fields = ('cantidad', 'comentario', 'insumo', 'usuario', 'fecha')


#modal agregar categoria en insumo nuevo
class insumoaddcat(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ('nombre',)
		labels = {
			'nombre': ('Nombre de categoria'),
		}



class editinsumoform(forms.ModelForm):
    class Meta:
		model = Insumo
		fields = ('nombre', 'codigo', 'descripcion', 'categoria', 'unidad', 'costounitario')
        #exclude = ('orden',)
		labels = {					
			'descripcion': ('Descripción'),
			'costounitario': ('Costo Unitario'),
			}
		widgets = {
			'costounitario': forms.TextInput(),
		}

class OrdenForm(forms.ModelForm):
	fecha = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	class Meta:
		model = OrdenCompra
		fields = ('proveedor', 'numero', 'orden', 'fecha', 'iva')
		labels = {
            'proveedor': ('Proveedor'),
            'numero': ('Numero de Orden'),
            'Orden': ('Orden'),
            'Fecha': ('Fecha'),
            'IVA': ('IVA'),
        }



class ProveeForm(forms.ModelForm):
	class Meta:
		model = Proveedor
		fields = ('nombre', 'id_unico', 'email', 'tel', 'direccion', 'celular')
	

class addinsumo(forms.ModelForm):
	class Meta:
		model = OrdenConcepto
		fields = ('insumo', 'orden', 'cantidad')
	


class OrdenCompraModificar(forms.ModelForm):
	fecha = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}), required=False, input_formats=['%Y-%m-%d','%m/%d/%Y', '%m/%d/%y'])
	class Meta:
		model = OrdenCompra
		fields = ('proveedor', 'numero', 'orden', 'fecha', 'iva')
		labels = {
            'proveedor': ('Proveedor'),
            'numero': ('Numero de Orden'),
            'Orden': ('Orden'),
            'Fecha': ('Fecha'),
            'IVA': ('IVA'),
        }


class editinsumocompra(forms.ModelForm):
	class Meta:
		model = OrdenConcepto
		fields = ('insumo', 'orden', 'cantidad')
	






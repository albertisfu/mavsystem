from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from forms import *
import django_filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from django.shortcuts import get_object_or_404

from django.core.urlresolvers import reverse

@login_required
def altaProducto(request):
	template =  get_template("altaproducto.html")
	form = altaProductoForm()
	context = {
	'form': form,
	}
	if 'save' in request.POST:
		form = altaProductoForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save()
			post.save()

	return HttpResponse(template.render(context, request))




class ProductosFilter(django_filters.FilterSet):

	class Meta:
		model = Producto
		fields = { #creamos los filtros necesarios 
        		  'categoria':['exact'],
        		 }




@login_required
def listaProducto(request):
	filters = ProductosFilter(request.GET, queryset=Producto.objects.all()) 
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		productos= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		productos = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		productos = paginator.page(paginator.num_pages)
	template =  get_template("listaproductos.html")
	context = {
		'productos': productos,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))



@login_required
def ProductoDetail(request, producto):
	producto = get_object_or_404(Producto, pk = producto) 
	template =  get_template("productodetail.html")
	materials = InsumoProducto.objects.filter(producto=producto)
	paginator = Paginator(materials, 20)
	page = request.GET.get('page')
	try:
		materiales= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		materiales = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		materiales = paginator.page(paginator.num_pages)


	context = {
        'producto': producto, 'materiales': materiales,
    }
	return HttpResponse(template.render(context, request))






@login_required
def ProductoInsumo(request, producto):
	producto = get_object_or_404(Producto, pk = producto)
	template =  get_template("productoinsumo.html")
	form = ProductoInsumoForm(initial={'producto':producto})
	form.fields['producto'].widget = forms.HiddenInput()
	context = {
		'producto':producto,'form': form,
	}
	if 'save' in request.POST:
		
		form = ProductoInsumoForm(request.POST)
		cantidad = request.POST['cantidad']
		print cantidad
		if form.is_valid():
			form.save()
			#post.save() revisar en plataforma, se guarda 2 veces
			print 'guardado'
			return HttpResponseRedirect(reverse('ProductoDetail', args=(producto.id,)))

	return HttpResponse(template.render(context, request))




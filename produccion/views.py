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
from almacen.models import Insumo
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
		insumopk = request.POST['insumo']
		insumo = get_object_or_404(Insumo, pk = insumopk) 
		print insumo
		insumoproducto= InsumoProducto.objects.create(insumo=insumo, producto=producto, cantidad=cantidad)
		print 'guardado'
		return HttpResponseRedirect(reverse('ProductoDetail', args=(producto.id,)))
	return HttpResponse(template.render(context, request))




class InsumosFilter(django_filters.FilterSet):

	class Meta:
		model = Insumo
		fields = { #creamos los filtros necesarios 
        		  'categoria':['exact'],
        		 }


@login_required
def popInsumo(request):
	filters = InsumosFilter(request.GET, queryset=Insumo.objects.all()) 
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		insumos= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		insumos = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		insumos = paginator.page(paginator.num_pages)

	context = {'insumos': insumos,'filters': filters,
	}
	template =  get_template("popinsumo.html")
	return HttpResponse(template.render(context, request))





class InsumoPopListView(ListView):
	model = Insumo
	template_name = 'listpop_list.html'
  
import operator
from django.db.models import Q
class SearchPopListView(InsumoPopListView):
    paginate_by = 5

    def get_queryset(self):
        result = super(SearchPopListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombre__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(codigo__icontains=q) for q in query_list))
            )

        return result



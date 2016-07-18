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

from django.shortcuts import get_object_or_404, redirect

from django.core.urlresolvers import reverse

@login_required
def altaProducto(request):
	template =  get_template("altaproducto.html")
	form = altaProductoForm()

	if 'save' in request.POST:
		form = altaProductoForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save()
			post.save()
			return redirect('listaProducto')

	form2 = productoaddcat()
	if 'save1' in request.POST:
		form2 = productoaddcat(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('altaProducto'))
		else:
			print 'error'
			print form.errors, len(form.errors)

	context = {
	'form': form, 'form2' : form2,
	}

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
	form = CostoEspecialForm(initial={'producto':producto})
	form.fields['producto'].widget = forms.HiddenInput()
	if 'save' in request.POST:
		form = CostoEspecialForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('ProductoDetail', args=(producto.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)

	costoespeciales = CostoEspecial.objects.filter(producto=producto)[:15]

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
        'producto': producto, 'materiales': materiales, 'form':form, 'costoespeciales':costoespeciales,
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



#Ordenes Views

@login_required
def altaOrden(request):
	current_user = request.user
	template =  get_template("altaorden.html")
	form = altaOrdenForm(initial={'usuario':current_user})
	form.fields['usuario'].widget = forms.HiddenInput()
	#context = {
	#'form': form,
	#}
	if 'save' in request.POST:
		form = altaOrdenForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return redirect('listaOrdenes')
		#else:
		#	print 'error'
		#	print form.errors, len(form.errors)

	form2 = addcliente()
	if 'save1' in request.POST:
		form2 = addcliente(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('altaOrden'))
		else:
			print 'error'
			print form.errors, len(form.errors)

	context = {
	'form': form, 'form2' : form2,
	}

	return HttpResponse(template.render(context, request))


class OrdenesFilter(django_filters.FilterSet):
	class Meta:
		model = Orden
		fields = { #creamos los filtros necesarios 
        		  'estatus':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-fecha_entrega', 'Fecha de entrega menor'),
				    ('fecha_entrega', 'Fecha de entrega mayor'),
				    ('-fecha_expedicion', 'Fecha de expedicion menor'),
				    ('fecha_expedicion', 'Fecha de expedicion mayor'),

				)





@login_required
def listaOrdenes(request):
	filters = OrdenesFilter(request.GET, queryset=Orden.objects.all()) 
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		ordenes= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		ordenes = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		ordenes = paginator.page(paginator.num_pages)
	template =  get_template("listaordenes.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))



@login_required
def OrdenDetail(request, orden):
	current_user = request.user
	orden = get_object_or_404(Orden, pk = orden) 
	template =  get_template("ordendetail.html")
	productos = ProductoOrden.objects.filter(orden=orden)
	form = comentarioOrdenForm(initial={'usuario':current_user, 'orden':orden})
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['orden'].widget = forms.HiddenInput()

	if 'save' in request.POST:
		form = comentarioOrdenForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('OrdenDetail', args=(orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)

	comentarios = ComentariosOrden.objects.filter(orden=orden)[:15] #solamente los ultimos 5 comentarios
	paginator = Paginator(productos, 5)
	page = request.GET.get('page')
	try:
		productos= paginator.page(page)
	except PageNotAnInteger:
		# Si la pagina no es un entero muestra la primera pagina
		productos = paginator.page(1)
	except EmptyPage:
		# si la pagina esta fuera de rango, muestra la ultima pagina
		productos = paginator.page(paginator.num_pages)

	context = {
		'orden': orden, 'productos': productos, 'comentarios': comentarios, 'form':form,
	}

	return HttpResponse(template.render(context, request))






@login_required
def OrdenProducto(request, orden):
	orden = get_object_or_404(Orden, pk = orden)
	template =  get_template("ordenproducto.html")
	#form = OrdenProductoForm(initial={'orden':orden})
	#form.fields['orden'].widget = forms.HiddenInput()

	context = {
		'orden':orden,
	}
	if 'save' in request.POST:
		cantidad = request.POST['cantidad']
		unidad = request.POST['unidad']
		color = request.POST['color']
		comentario = request.POST['comentario']

		print cantidad
		productopk = request.POST['producto']
		producto = get_object_or_404(Producto, pk = productopk) 
		print producto
		productoorden= ProductoOrden.objects.create(producto=producto, orden=orden, unidad=unidad, cantidad=cantidad, color=color, comentario=comentario)
		print 'guardado'
		return HttpResponseRedirect(reverse('OrdenDetail', args=(orden.id,)))
	return HttpResponse(template.render(context, request))



@login_required
def OrdenProductoDetail(request, producto):
	current_user = request.user
	producto_orden = get_object_or_404(ProductoOrden, pk = producto)
	orden = get_object_or_404(Orden, pk = producto_orden.orden.id)
	insumos = InsumoProducto.objects.filter(producto=producto_orden.producto)
	checkinsumos = CheckInsumoProducto.objects.filter(productorden=producto_orden)
	template =  get_template("ordenproductodetail.html")
	#form = OrdenProductoForm(initial={'orden':orden})
	#form.fields['orden'].widget = forms.HiddenInput()

	costoespeciales = CostoEspecial.objects.filter(producto=producto_orden.producto)[:15]

	form = estatusProductoInsumo(initial={'usuario':current_user, 'productorden':producto_orden})
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['productorden'].widget = forms.HiddenInput()
	form.fields['insumo'].widget = forms.HiddenInput()

	if 'save' in request.POST:
		form = estatusProductoInsumo(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('OrdenProductoDetail', args=(producto_orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)


	paginator = Paginator(insumos, 20)
	page = request.GET.get('page')
	try:
		insumos= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		insumos = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		insumos = paginator.page(paginator.num_pages)


	context = {
		'orden':orden, 'producto_orden':producto_orden, 'insumos':insumos, 'checkinsumos':checkinsumos, 'form':form, 'costoespeciales':costoespeciales,
	}
	
	return HttpResponse(template.render(context, request))

@login_required
def HistoryCheckInsumo(request, orden, insumo):
	producto_orden = get_object_or_404(ProductoOrden, pk = orden)
	insumo_producto =  get_object_or_404(InsumoProducto, pk = insumo)
	print producto_orden
	print insumo_producto
	insumos = CheckInsumoProducto.objects.filter(insumo=insumo_producto, productorden=producto_orden)
	template =  get_template("checkinsumos.html")
	#form = OrdenProductoForm(initial={'orden':orden})
	#form.fields['orden'].widget = forms.HiddenInput()

	paginator = Paginator(insumos, 20)
	page = request.GET.get('page')
	try:
		insumos= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		insumos = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		insumos = paginator.page(paginator.num_pages)


	context = { 'insumos':insumos,
	}
	
	return HttpResponse(template.render(context, request))








#search


class OrdenesListView(ListView):
	model = Orden
	template_name = 'ordenes_list.html'
  

import operator
from django.db.models import Q
class SearchOrdenesListView(OrdenesListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(SearchOrdenesListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombre__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(codigo__icontains=q) for q in query_list))|
                reduce(operator.and_,
                       (Q(cliente__nombrecontacto__icontains=q) for q in query_list))
            )

        return result




class ProductosFilter(django_filters.FilterSet):

	class Meta:
		model = Producto
		fields = { #creamos los filtros necesarios 
        		  'categoria':['exact'],
        		 }


@login_required
def popProducto(request):
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

	context = {'productos': productos,'filters': filters,
	}
	template =  get_template("pop_product.html")
	return HttpResponse(template.render(context, request))


class ProductoPopListView(ListView):
	model = Producto
	template_name = 'listpop_list.html'
  
import operator
from django.db.models import Q
class SearchProductoPopListView(ProductoPopListView):
    paginate_by = 5

    def get_queryset(self):
        result = super(SearchProductoPopListView, self).get_queryset()

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

from django.views.decorators.csrf import csrf_exempt
from json import dumps
@csrf_exempt
def ajaxInsumo(request):
	if request.method == 'POST':
		print 'entroajax'
		pkinsumo = request.POST['pk']
		insumo = get_object_or_404(Insumo, pk = pkinsumo)
		insumonombre =  insumo.nombre
		insumocodigo = insumo.codigo
		data = [{'insumo':insumonombre}, {'insumosku':insumocodigo}] 
		#print data
        return HttpResponse(dumps(data))


@csrf_exempt
def ajaxProducto(request):
	if request.method == 'POST':
		print 'entroajax'
		pkproducto = request.POST['pk']
		producto = get_object_or_404(Producto, pk = pkproducto)
		productonombre =  producto.nombre
		productocodigo = producto.codigo
		data = [{'producto':productonombre}, {'productosku':productocodigo}] 
		#print data
        return HttpResponse(dumps(data))



#Lista cliente



@login_required
def listaClientes(request):
	filters = Cliente.objects.all()
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		clientes= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		clientes = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		clientes = paginator.page(paginator.num_pages)
	template =  get_template("listaclientes.html")
	context = {
		'clientes': clientes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))





#search clientes


class ClientesListView(ListView):
	model = Cliente
	template_name = 'clientes_list.html'
  

import operator
from django.db.models import Q
class SearchClientesListView(ClientesListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(SearchClientesListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(nombrecontacto__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(empresainstitucion__icontains=q) for q in query_list))|
                reduce(operator.and_,
                       (Q(email__icontains=q) for q in query_list))
            )

        return result





@login_required
def ClienteDetail(request, cliente):
	cliente = get_object_or_404(Cliente, pk = cliente) 
	template =  get_template("clientedetail.html")
	ordenes = Orden.objects.filter(cliente=cliente)
	paginator = Paginator(ordenes, 5)
	page = request.GET.get('page')
	try:
		ordenes= paginator.page(page)
	except PageNotAnInteger:
		# Si la pagina no es un entero muestra la primera pagina
		ordenes = paginator.page(1)
	except EmptyPage:
		# si la pagina esta fuera de rango, muestra la ultima pagina
		ordenes = paginator.page(paginator.num_pages)

	context = {
		'ordenes': ordenes, 'cliente': cliente,
	}

	return HttpResponse(template.render(context, request))



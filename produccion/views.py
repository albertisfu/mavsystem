# -*- coding: utf-8 -*-
from django.shortcuts import render
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

from django.contrib.auth.decorators import login_required, user_passes_test #permisos y grupos
from django.utils.decorators import method_decorator #permisos y grupos

#impresion
from weasyprint import HTML, CSS
from django.conf import settings

# ---------------------------------------------------------
# ---------------------------------------------------------
#Grupos, checar si pertenece a grupo

def group_required(*group_names):
	def check(user):
		if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
			return True
		else:
			return False
	return user_passes_test(check, login_url='/prohibido/')

# ---------------------------------------------------------
# ---------------------------------------------------------
# Alta producto


@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def altaProducto(request):
	template =  get_template("alta_producto.html")
	form = altaProductoForm()

	if 'save' in request.POST:
		form = altaProductoForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save()
			post.save()
			#return redirect('listaProducto')
			return HttpResponseRedirect(reverse('ProductoDetail', args=(post.id,)))
		else:
			print "Error en alta de producto"
			print form.errors

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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Filtro lista productos

class ProductosFilter(django_filters.FilterSet):

	class Meta:
		model = Producto
		fields = { #creamos los filtros necesarios 
				  'categoria':['exact'],
				 }


# ---------------------------------------------------------
# ---------------------------------------------------------
# Lista de producto

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
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
	template =  get_template("lista_productos.html")
	context = {
		'productos': productos,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Detalle de producto

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def ProductoDetail(request, producto):
	producto = get_object_or_404(Producto, pk = producto) 
	template =  get_template("detalle_producto.html")
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




# ---------------------------------------------------------
# ---------------------------------------------------------
# Editar Producto
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EditarProducto(request, pk):


	post = get_object_or_404(Producto, pk=pk)

	if 'save' in request.POST:
		form = altaProductoForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save()
			post.save()
			#return redirect('listaProducto')
			return HttpResponseRedirect(reverse('ProductoDetail', args=(pk,)))
		else:
			print "Error en edición de producto"
			print form.errors
	else:
		form = altaProductoForm(instance=post)

	form2 = productoaddcat()
	if 'save1' in request.POST:
		form2 = productoaddcat(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('EditarProducto', args=(pk,)))
		else:
			print 'error'
			print form.errors, len(form.errors)
	else:
		form2 = productoaddcat()
	
	# post = get_object_or_404(ProductoAlmacenMod, pk=pk)
 #        if request.method == "POST":
 #            form = ProductoMod(request.POST, instance=post)
 #            if form.is_valid():
 #                post = form.save(commit=False)
 #                post.author = request.user
 #                post.save()
 #                return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(productos,)))
 #        else:
 #            form = ProductoMod(instance=post)
        return render(request, 'editar_producto.html', {'form': form, 'form2':form2, 'prod':post.pk})


# ---------------------------------------------------------
# ---------------------------------------------------------
# Detalle de producto > Asignar Material

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def ProductoInsumo(request, producto):
	producto = get_object_or_404(Producto, pk = producto)
	template =  get_template("productoinsumo.html")
	form = ProductoInsumoForm(initial={'producto':producto})
	form.fields['producto'].widget = forms.HiddenInput()
	context = {
		'producto':producto,'form': form,
	}
	if request.method == 'POST':
	#if 'save' in request.POST:
		form = ProductoInsumoForm(request.POST)
		if form.is_valid():
			
			cantidad = request.POST['cantidad']
			print cantidad
			insumopk = request.POST['insumo']
			insumo = get_object_or_404(Insumo, pk = insumopk) 
			print insumo
			insumoproducto= InsumoProducto.objects.create(insumo=insumo, producto=producto, cantidad=cantidad)
			print 'guardado'
			return HttpResponseRedirect(reverse('ProductoDetail', args=(producto.id,)))
		else:
			print "Error en el form"
			print form.errors

	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Detalle de producto > asignar material > popup filtro

class InsumosFilter(django_filters.FilterSet):

	class Meta:
		model = Insumo
		fields = { #creamos los filtros necesarios 
				  'categoria':['exact'],
				 }


# ---------------------------------------------------------
# ---------------------------------------------------------
# Detalle de producto > asignar material > popup lista

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
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

# ---------------------------------------------------------
# ---------------------------------------------------------
# Detalle de producto > asignar material > popup buscar

class InsumoPopListView(ListView):
	model = Insumo
	template_name = 'listpop_list.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion', 'Ventas'))
	def dispatch(self, *args, **kwargs):
		return super(InsumoPopListView, self).dispatch(*args, **kwargs)
  
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

#Cotizaciones Produccion ***************-------------*****

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista cotizaciones - filtros

class CotizacionesFilter(django_filters.FilterSet):
	class Meta:
		model = Cotizacion
		fields = { #creamos los filtros necesarios 
				  'estatus':['exact'],
				 }


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista cotizaciones
# /ventas/lista-cotizaciones

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def listaCotizacionesVentas(request):
	filters = CotizacionesFilter(request.GET, queryset=Cotizacion.objects.filter(estatus=2)) #cotizaciones completadas
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
	template =  get_template("lista_cotizaciones_ventas.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion
# /ventas/cotizacion/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def CotizacionDetailVentas(request, orden):
	current_user = request.user
	orden = get_object_or_404(Cotizacion, pk = orden) 
	template =  get_template("detalle_cotizacion_ventas.html")
	productos = ProductoCotizacion.objects.filter(orden=orden)
	estatus = 2 #completada
	comentario = 'Completada'
	form = comentarioCotizacionForm(initial={'usuario':current_user, 'orden':orden, 'estatus':estatus, 'comentario':comentario})
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['orden'].widget = forms.HiddenInput()
	form.fields['estatus'].widget = forms.HiddenInput()
	form.fields['comentario'].widget = forms.HiddenInput()

	formventa = altaOrdenForm(initial={'usuario':current_user})
	formventa.fields['usuario'].widget = forms.HiddenInput()

	if 'venta' in request.POST:
		formventa = altaOrdenForm(request.POST)
		print request.POST
		if formventa.is_valid():
			print 'valid'
			ins = formventa.save()
			print ins.pk
			for producto in productos:
				productoorden= ProductoOrden.objects.create(content_type_id=24, object_id=producto.id , orden=ins, unidad=producto.unidad, cantidad=producto.cantidad, color=producto.color, comentario=producto.comentario)

			#return redirect('listaOrdenes')
			return HttpResponseRedirect(reverse('OrdenDetail', args=(ins.id,)))
		else:
			print 'error'
			print formventa.errors, len(formventa.errors)


	if 'save' in request.POST:
		form = comentarioCotizacionForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('CotizacionDetailProduccion', args=(orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)

	comentarios = ComentariosCotizacion.objects.filter(orden=orden)[:15] #solamente los ultimos 5 comentarios
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
		'orden': orden, 'productos': productos, 'comentarios': comentarios, 'form':form, 'formventa':formventa
	}

	return HttpResponse(template.render(context, request))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista cotizaciones
# /administrador/lista-cotizaciones

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def listaCotizacionesProduccion(request):
	filters = CotizacionesFilter(request.GET, queryset=Cotizacion.objects.all()) 
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
	template =  get_template("lista_cotizaciones_produccion.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion
# /administrador/cotizacion/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def CotizacionDetailProduccion(request, orden):
	current_user = request.user
	orden = get_object_or_404(Cotizacion, pk = orden) 
	template =  get_template("detalle_cotizacion_produccion.html")
	productos = ProductoCotizacion.objects.filter(orden=orden)
	estatus = 2 #completada
	comentario = 'Completada'
	form = comentarioCotizacionForm(initial={'usuario':current_user, 'orden':orden, 'estatus':estatus, 'comentario':comentario})
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['orden'].widget = forms.HiddenInput()
	form.fields['estatus'].widget = forms.HiddenInput()
	form.fields['comentario'].widget = forms.HiddenInput()

	if 'save' in request.POST:
		form = comentarioCotizacionForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('CotizacionDetailProduccion', args=(orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)

	comentarios = ComentariosCotizacion.objects.filter(orden=orden)[:15] #solamente los ultimos 5 comentarios
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




# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion > Agregar producto
# /administrador/cotizacion/asignar-producto/pk/


from django.db.models.signals import post_save

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def CotizacionProductoProduccion(request, orden):
	orden = get_object_or_404(Cotizacion, pk = orden)
	template =  get_template("asignar_producto_cotizacion.html")
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
		productomod = ProductoCotizacionMod.objects.create(orden=orden, producto=producto, nombre=producto.nombre, codigo=producto.codigo, descripcion=producto.descripcion, categoria=producto.categoria, costo=producto.costo, precio_venta=producto.precio_venta, file=producto.file) 
		insumos = InsumoProducto.objects.filter(producto=producto)

		costos_especiales = CostoEspecial.objects.filter(producto=producto)

		for costo in costos_especiales:
			costomod = CostoEspecialCotizacion.objects.create(producto=productomod, concepto=costo.concepto, costo=costo.costo)

		for insumo in insumos:
			# crear insumo para producto duplicado
			insumomod = InsumoCotizacionMod.objects.create(insumo=insumo.insumo, producto=productomod, cantidad=insumo.cantidad, costototal=insumo.costototal)
			print insumomod


		#print producto
		productoorden= ProductoCotizacion.objects.create(producto=productomod, orden=orden, unidad=unidad, cantidad=cantidad, color=color, comentario=comentario)
		print 'guardado'
		return HttpResponseRedirect(reverse('CotizacionDetailProduccion', args=(orden.id,)))
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion > Detalle de producto
# /produccion/cotizacion/productos-cotizacion/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def CotizacionProductoDetailProduccion(request, producto):
	current_user = request.user
	producto_orden = get_object_or_404(ProductoCotizacion, pk = producto)
	orden = get_object_or_404(Cotizacion, pk = producto_orden.orden.id)
	insumos = InsumoCotizacionMod.objects.filter(producto=producto_orden.producto)
	pk = producto
	template =  get_template("detalle_producto_cotizacion.html")
	#form = OrdenProductoForm(initial={'orden':orden})
	#form.fields['orden'].widget = forms.HiddenInput()

	form1 = CostoEspecialCotizacionForm(initial={'producto':producto_orden.producto.pk})
	form1.fields['producto'].widget = forms.HiddenInput()
	if 'save' in request.POST:
		form1 = CostoEspecialCotizacionForm(request.POST)
		print request.POST
		if form1.is_valid():
			print 'valid'
			form1.save()
			return HttpResponseRedirect(reverse('CotizacionProductoDetailProduccion', args=(producto_orden.id,)))
		else:
			print 'error'
			print form1.errors, len(form1.errors)



	costoespeciales = CostoEspecialCotizacion.objects.filter(producto=producto_orden.producto)[:15]

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
		'form1':form1,'pk':pk, 'orden':orden, 'producto_orden':producto_orden, 'costoespeciales':costoespeciales,'insumos':insumos,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Asignar Material

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def ProductoInsumoProduccionCotizacion(request, productoalmacen):
	productocot = get_object_or_404(ProductoCotizacion, pk = productoalmacen)
	producto = productocot.producto
	template =  get_template("producto_insumo_almacen.html")
	form = ProductoInsumoCotizacionForm(initial={'producto':producto})
	form.fields['producto'].widget = forms.HiddenInput()
	context = {
		'producto':producto,'form': form,
	}
	if request.method == 'POST':
	#if 'save' in request.POST:
		form = ProductoInsumoCotizacionForm(request.POST)
		if form.is_valid():
			
			cantidad = request.POST['cantidad']
			print cantidad
			insumopk = request.POST['insumo']
			insumo = get_object_or_404(Insumo, pk = insumopk) 
			print insumo
			insumoproducto= InsumoCotizacionMod.objects.create(insumo=insumo, producto=producto, cantidad=cantidad)
			print 'guardado'
			return HttpResponseRedirect(reverse('CotizacionProductoDetailProduccion', args=(productocot.id,)))
		else:
			print "Error en el form"
			print form.errors

	return HttpResponse(template.render(context, request))


from django.http import Http404  
# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Eliminar Material

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EliminarProductoInsumoProduccionCotizacion(request, pk, producto):
	productocot = get_object_or_404(ProductoCotizacion, pk = producto)
	producto = productocot.producto
	try:
		insumos = InsumoCotizacionMod.objects.get(pk=pk, producto=producto)
	except:
		raise Http404 
	else:
		
		insumos.delete()
		print 'insumo eliminado'
		return HttpResponseRedirect(reverse('CotizacionProductoDetailProduccion', args=(productocot.pk,)))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Editar Material
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EditarProductoInsumoProduccionCotizacion(request, pk, producto):
	
	post = get_object_or_404(InsumoCotizacionMod, pk=pk)
        if request.method == "POST":
            form = InsumoModCot(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('CotizacionProductoDetailProduccion', args=(producto,)))
        else:
            form = InsumoMod(instance=post)
        return render(request, 'editar_almacen_insumo.html', {'form': form})


# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Eliminar Costo Especial
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EliminarCostoEspecialProduccionCotizacion(request, pk, producto):
	try:
		insumos = CostoEspecialCotizacion.objects.get(pk=pk)
	except:
		#return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto,)))
		raise Http404 
	else:
		insumos.delete()
		print 'insumo eliminado'
		return HttpResponseRedirect(reverse('CotizacionProductoDetailProduccion', args=(producto,)))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Editar Producto
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EditarProductoProduccionCotizacion(request, pk, producto):

	post = get_object_or_404(ProductoCotizacionMod, pk=pk)

	if 'save' in request.POST:
		form = ProductoModCot(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save()
			post.save()
			#return redirect('listaProducto')
			return HttpResponseRedirect(reverse('CotizacionProductoDetailProduccion', args=(producto,)))
		else:
			print "Error en edición de producto"
			print form.errors
	else:
		form = ProductoModCot(instance=post)

	form2 = productoaddcat()
	if 'save1' in request.POST:
		form2 = productoaddcat(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('EditarProductoAlmacen', args=(producto,pk)))
		else:
			print 'error'
			print form.errors, len(form.errors)
	else:
		form2 = productoaddcat()
	
	# post = get_object_or_404(ProductoAlmacenMod, pk=pk)
 #        if request.method == "POST":
 #            form = ProductoMod(request.POST, instance=post)
 #            if form.is_valid():
 #                post = form.save(commit=False)
 #                post.author = request.user
 #                post.save()
 #                return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(productos,)))
 #        else:
 #            form = ProductoMod(instance=post)
        return render(request, 'editar_almacen_producto.html', {'form': form, 'form2':form2, 'prod':producto})

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion > Vista de impresion
# /administrador/cotizacion/imprimir/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def cotizacion_impresion_produccion(request, orden):
	orden = get_object_or_404(Cotizacion, pk = orden) 
	productos = ProductoCotizacion.objects.filter(orden=orden)
	mediaurl = getattr(settings, 'MEDIA_URL', None)
	contexto = {'orden':orden,'productos':productos, 'mediaurl':mediaurl}
	template = get_template('imprimir_cotizacion.html')
	rendered_html = template.render(contexto).encode(encoding="ISO-8859-1")
	pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  '/css/pdf.css')])
	http_response = HttpResponse(rendered_html, content_type='text/html')
	return http_response 



# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista de cotizaciones > buscador


class CotizacionesListViewProduccion(ListView):
	model = Cotizacion
	template_name = 'buscar_cotizacion_produccion.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion', 'Ventas'))
	def dispatch(self, *args, **kwargs):
		return super(CotizacionesListViewProduccion, self).dispatch(*args, **kwargs)
  

import operator
from django.db.models import Q
class SearchCotizacionesListViewProduccion(CotizacionesListViewProduccion):
	"""
	Display a Blog List page filtered by the search query.
	"""
	paginate_by = 10

	def get_queryset(self):
		result = super(SearchCotizacionesListViewProduccion, self).get_queryset()

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



#********------------Termina Cotizacion Produccion ***********


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Nueva orden
# /administrador/alta_orden

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def altaOrden(request):
	current_user = request.user
	template =  get_template("alta_orden.html")
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
			ins = form.save()
			#return redirect('listaOrdenes')
			return HttpResponseRedirect(reverse('OrdenDetail', args=(ins.id,)))
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

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista ordenes - filtros

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

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista ordenes
# /administrador/lista_ordenes

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
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
	template =  get_template("lista_ordenes.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden
# /administrador/orden/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def OrdenDetail(request, orden):
	current_user = request.user
	orden = get_object_or_404(Orden, pk = orden) 
	template =  get_template("detalle_orden.html")
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

	if 'pkp' in request.POST:
		productocot = get_object_or_404(ProductoCotizacionMod, pk=request.POST['pkp'])
		productocot.precio_venta = request.POST['precio']
		productocot.save()
		total = 0
		for productove in productos:
			if productove.content_type_id == 13: #producto linea

				total = (productove.content_object.precio_venta * productove.cantidad) + total

			elif productove.content_type_id == 24: #producto cotizacion

				total = (productove.content_object.producto.precio_venta * productove.cantidad) + total
			orden.costo = total
			orden.save()


		print 'pkp'

	if 'confirm' in request.POST:
		orden.estatus = 2
		orden.save()
		ordenal=OrdenAlmacen.objects.create(nombre = orden.nombre, codigo = orden.codigo, descripcion=orden.descripcion, cliente=orden.cliente, fecha_entrega=orden.fecha_entrega, estatus = 1, usuario=request.user, costo=orden.costo, fecha_entrega_almacen=orden.fecha_entrega_almacen, nota=orden.nota)

		for producto in productos:
			if producto.content_type_id==13: #si es un producto de linea
				productomod = ProductoAlmacenMod.objects.create(orden=ordenal, producto=producto.content_object, nombre=producto.content_object.nombre, codigo=producto.content_object.codigo, descripcion=producto.content_object.descripcion, categoria=producto.content_object.categoria, costo=producto.content_object.costo, precio_venta=producto.content_object.precio_venta, file=producto.content_object.file)
				insumos = InsumoProducto.objects.filter(producto=producto.content_object)
				costos_especiales = CostoEspecial.objects.filter(producto=producto.content_object)
				for costo in costos_especiales:
					costomod = CostoEspecialAlmacen.objects.create(producto=productomod, concepto=costo.concepto, costo=costo.costo)

				for insumo in insumos:
					# crear insumo para producto duplicado
					insumomod = InsumoProductoMod.objects.create(insumo=insumo.insumo, producto=productomod, cantidad=insumo.cantidad, costototal=insumo.costototal)
					print insumomod
				productoorden= ProductoOrdenAlmacen.objects.create(producto=productomod, orden=ordenal, unidad=producto.unidad, cantidad=producto.cantidad, color=producto.color, comentario=producto.comentario)


			elif producto.content_type_id==24: #si es un producto de cotizacion
				productomod = ProductoAlmacenMod.objects.create(orden=ordenal, producto=producto.content_object.producto.producto, nombre=producto.content_object.producto.nombre, codigo=producto.content_object.producto.codigo, descripcion=producto.content_object.producto.descripcion, categoria=producto.content_object.producto.categoria, costo=producto.content_object.producto.costo, precio_venta=producto.content_object.producto.precio_venta, file=producto.content_object.producto.file)
				insumos = InsumoCotizacionMod.objects.filter(producto=producto.content_object.producto)
				costos_especiales = CostoEspecialCotizacion.objects.filter(producto=producto.content_object.producto)
				for costo in costos_especiales:
					costomod = CostoEspecialAlmacen.objects.create(producto=productomod, concepto=costo.concepto, costo=costo.costo)

				for insumo in insumos:
					# crear insumo para producto duplicado
					insumomod = InsumoProductoMod.objects.create(insumo=insumo.insumo, producto=productomod, cantidad=insumo.cantidad, costototal=insumo.costototal)
					print insumomod
				productoorden= ProductoOrdenAlmacen.objects.create(producto=productomod, orden=ordenal, unidad=producto.unidad, cantidad=producto.cantidad, color=producto.color, comentario=producto.comentario)

		print 'confirm creacion'

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

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > Vista de impresion
# /administrador/orden/imprimir/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def orden_impresion(request, orden):
	orden = get_object_or_404(Orden, pk = orden) 
	productos = ProductoOrden.objects.filter(orden=orden)
	mediaurl = getattr(settings, 'MEDIA_URL', None)
	contexto = {'orden':orden,'productos':productos, 'mediaurl':mediaurl}
	template = get_template('imprimir_orden.html')
	rendered_html = template.render(contexto).encode(encoding="ISO-8859-1")
	pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  '/css/pdf.css')])
	http_response = HttpResponse(rendered_html, content_type='text/html')
	return http_response 



# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > Agregar producto
# /administrador/asignar_producto/pk/


from django.db.models.signals import post_save

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def OrdenProducto(request, orden):
	orden = get_object_or_404(Orden, pk = orden)
	template =  get_template("asignar_producto_orden.html")
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
		
		"""insumos = InsumoProducto.objects.filter(producto=producto)
		for insumo in insumos:
			print insumo
			total_insumos_producto = insumo.cantidad * int(cantidad)
			print total_insumos_producto
			if total_insumos_producto <= insumo.insumo.stock:
				print 'suficiente'
				newstock = insumo.insumo.stock - total_insumos_producto
				Insumo.objects.filter(pk=insumo.insumo.pk).update(stock=newstock)
				post_save.send(Insumo, instance=insumo.insumo, created=False) #signal update costo stock
			else:
				newstock = insumo.insumo.stock - total_insumos_producto
				Insumo.objects.filter(pk=insumo.insumo.pk).update(stock=newstock)
				post_save.send(Insumo, instance=insumo.insumo, created=False) #signal update costo stock
				print 'no alcanza'
			"""

		#print producto
		productoorden= ProductoOrden.objects.create(content_type_id =13 , object_id=producto.id , orden=orden, unidad=unidad, cantidad=cantidad, color=color, comentario=comentario)
		print 'guardado'
		return HttpResponseRedirect(reverse('OrdenDetail', args=(orden.id,)))
	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > Detalle de producto
# /administrador/producto_orden/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def OrdenProductoDetail(request, producto):
	current_user = request.user
	producto_orden = get_object_or_404(ProductoOrden, pk = producto)
	orden = get_object_or_404(Orden, pk = producto_orden.orden.id)
	if producto_orden.content_type_id==13: #producto linea
		
		insumos = InsumoProducto.objects.filter(producto=producto_orden.content_object)
		costoespeciales = CostoEspecial.objects.filter(producto=producto_orden.content_object)[:15]

	if producto_orden.content_type_id==24: #producto de coizacion
		

		insumos = InsumoCotizacionMod.objects.filter(producto=producto_orden.content_object.producto)
		costoespeciales = CostoEspecialCotizacion.objects.filter(producto=producto_orden.content_object.producto)[:15]


	#checkinsumos = CheckInsumoProducto.objects.filter(productorden=producto_orden)
	template =  get_template("detalle_producto_orden.html")
	#form = OrdenProductoForm(initial={'orden':orden})
	#form.fields['orden'].widget = forms.HiddenInput()

	

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
		 'producto_orden':producto_orden, 'insumos':insumos, 'form':form, 'costoespeciales':costoespeciales,
	}
	
	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > Detalle de producto > Historial
# /administrador/producto_orden/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
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



# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista de ordenes > buscador


class OrdenesListView(ListView):
	model = Orden
	template_name = 'buscar_orden.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion', 'Ventas'))
	def dispatch(self, *args, **kwargs):
		return super(OrdenesListView, self).dispatch(*args, **kwargs)
  

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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > popup producto filtros

class ProductosFilter(django_filters.FilterSet):

	class Meta:
		model = Producto
		fields = { #creamos los filtros necesarios 
				  'categoria':['exact'],
				 }

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > popup filtros

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > popup producto buscar

class ProductoPopListView(ListView):
	model = Producto
	template_name = 'listpop_list.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion', 'Ventas'))
	def dispatch(self, *args, **kwargs):
		return super(ProductoPopListView, self).dispatch(*args, **kwargs)
  
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



# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista de clientes

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
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
	template =  get_template("lista_clientes.html")
	context = {
		'clientes': clientes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))




# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista de clientes - buscador


class ClientesListView(ListView):
	model = Cliente
	template_name = 'buscar_clientes.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion', 'Ventas'))
	def dispatch(self, *args, **kwargs):
		return super(ClientesListView, self).dispatch(*args, **kwargs)
  

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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalles de cliente


@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def ClienteDetail(request, cliente):
	cliente = get_object_or_404(Cliente, pk = cliente) 
	template =  get_template("detalle_cliente.html")
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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Agregar cliente
# /administrador/alta_cliente

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def altaCliente(request):
	template =  get_template("agregar_cliente.html")
	if request.method == 'POST':
		form = addcliente(request.POST)
		if form.is_valid():
			print 'valid'
			form.save()
			return redirect('listaClientes')
		else:
			print 'error'
			print form.errors, len(form.errors)
	else:
		form = addcliente()

	context = {'form': form}

	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Nueva corizacion
# /administrador/alta-cotizacion

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def altaCotizacion(request):
	current_user = request.user
	template =  get_template("alta_cotizacion.html")

	if 'save' in request.POST:
		form = altaCotizacionForm(request.POST)
		print request.POST
		if form.is_valid():
			ins = form.save(commit=False)
			print 'valid'
			ins.usuario = request.user
			ins.save()
			return HttpResponseRedirect(reverse('CotizacionDetail', args=(ins.id,)))
	else:
		form = altaCotizacionForm()

	form2 = addcliente()
	if 'save1' in request.POST:
		form2 = addcliente(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('altaCotizacion'))
		else:
			print 'error'
			print form.errors, len(form.errors)
	else:
		form2 = addcliente()

	context = {
	'form': form, 'form2' : form2,
	}

	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista cotizaciones - filtros

class CotizacionesFilter(django_filters.FilterSet):
	class Meta:
		model = Cotizacion
		fields = { #creamos los filtros necesarios 
				  'estatus':['exact'],
				 }


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista cotizaciones
# /administrador/lista-cotizaciones

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def listaCotizaciones(request):
	filters = CotizacionesFilter(request.GET, queryset=Cotizacion.objects.all()) 
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
	template =  get_template("lista_cotizaciones.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion
# /administrador/cotizacion/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def CotizacionDetail(request, orden):
	current_user = request.user
	orden = get_object_or_404(Cotizacion, pk = orden) 
	template =  get_template("detalle_cotizacion.html")
	productos = ProductoCotizacion.objects.filter(orden=orden)
	estatus = 3 #cancelada
	form = comentarioCotizacionForm(initial={'usuario':current_user, 'orden':orden, 'estatus':estatus})
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['orden'].widget = forms.HiddenInput()
	form.fields['estatus'].widget = forms.HiddenInput()

	if 'save' in request.POST:
		form = comentarioCotizacionForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('CotizacionDetail', args=(orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)

	comentarios = ComentariosCotizacion.objects.filter(orden=orden)[:15] #solamente los ultimos 5 comentarios
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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion > Agregar producto
# /administrador/cotizacion/asignar-producto/pk/


from django.db.models.signals import post_save

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de cotizacion > Vista de impresion
# /administrador/cotizacion/imprimir/pk/

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def cotizacion_impresion(request, orden):
	orden = get_object_or_404(Cotizacion, pk = orden) 
	productos = ProductoCotizacion.objects.filter(orden=orden)
	mediaurl = getattr(settings, 'MEDIA_URL', None)
	contexto = {'orden':orden,'productos':productos, 'mediaurl':mediaurl}
	template = get_template('imprimir_cotizacion.html')
	rendered_html = template.render(contexto).encode(encoding="ISO-8859-1")
	pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  '/css/pdf.css')])
	http_response = HttpResponse(rendered_html, content_type='text/html')
	return http_response 


# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista de cotizaciones > buscador


class CotizacionesListView(ListView):
	model = Cotizacion
	template_name = 'buscar_cotizacion.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion', 'Ventas'))
	def dispatch(self, *args, **kwargs):
		return super(CotizacionesListView, self).dispatch(*args, **kwargs)
  

import operator
from django.db.models import Q
class SearchCotizacionesListView(CotizacionesListView):
	"""
	Display a Blog List page filtered by the search query.
	"""
	paginate_by = 10

	def get_queryset(self):
		result = super(SearchCotizacionesListView, self).get_queryset()

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


# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Nueva orden


@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def altaOrdenAlmacen(request):
	current_user = request.user
	template =  get_template("alta_orden_almacen.html")
	form = altaOrdenAlmacenForm(initial={'usuario':current_user})
	form.fields['usuario'].widget = forms.HiddenInput()
	#context = {
	#'form': form,
	#}
	if 'save' in request.POST:
		form = altaOrdenAlmacenForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			ins = form.save()
			#return redirect('listaOrdenes')
			return HttpResponseRedirect(reverse('OrdenAlmacenDetail', args=(ins.id,)))
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
			return HttpResponseRedirect(reverse('altaOrdenAlmacen'))
		else:
			print 'error'
			print form.errors, len(form.errors)

	context = {
	'form': form, 'form2' : form2,
	}

	return HttpResponse(template.render(context, request))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Lista ordenes - filtros

class OrdenesAlmacenFilter(django_filters.FilterSet):
	class Meta:
		model = OrdenAlmacen
		fields = { #creamos los filtros necesarios 
				  'estatus':['exact'],
				 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
					('-fecha_entrega', 'Fecha de entrega menor'),
					('fecha_entrega', 'Fecha de entrega mayor'),
					('-fecha_expedicion', 'Fecha de expedicion menor'),
					('fecha_expedicion', 'Fecha de expedicion mayor'),

				)


# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Lista ordenes


@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def listaOrdenesAlmacen(request):
	filters = OrdenesAlmacenFilter(request.GET, queryset=OrdenAlmacen.objects.all()) 
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
	template =  get_template("lista_ordenes_almacen.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de orden

from almacen.models import OrdenMateriales, OrdenMaterialesConcepto
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def OrdenAlmacenDetail(request, orden):
	current_user = request.user
	orden = get_object_or_404(OrdenAlmacen, pk = orden) 
	template =  get_template("detalle_orden_almacen.html")
	productos = ProductoOrdenAlmacen.objects.filter(orden=orden)
	form = comentarioOrdenAlmacenForm(initial={'usuario':current_user, 'orden':orden})
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['orden'].widget = forms.HiddenInput()

	if 'save' in request.POST:
		form = comentarioOrdenAlmacenForm(request.POST)
		print request.POST
		if form.is_valid():
			print 'valid'
			form.save()
			return HttpResponseRedirect(reverse('OrdenAlmacenDetail', args=(orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)


	if 'confirm' in request.POST:
		#orden.estatus = 2
		#orden.save()
		ordenal=OrdenMateriales.objects.create(orden=orden, numero = orden.codigo, estatus = 1, usuario=request.user)

		for producto in productos:
			insumos = InsumoProductoMod.objects.filter(producto=producto.producto)
				
			for insumo in insumos:
				# crear insumo para producto duplicado
				material = OrdenMaterialesConcepto.objects.create(insumo=insumo.insumo, orden=ordenal, cantidad=insumo.cantidad)
				
		print 'confirm creacion'



	comentarios = ComentariosOrdenAlmacen.objects.filter(orden=orden)[:15] #solamente los ultimos 5 comentarios
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



# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Detalle de orden > Agregar producto
# /administrador/asignar_producto/pk/


@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def OrdenAlmacenProducto(request, orden):
	orden = get_object_or_404(OrdenAlmacen, pk = orden)
	template =  get_template("asignar_producto_orden_almacen.html")
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
		producto = get_object_or_404(Producto, pk = productopk) # sacar producto original y despues crear producto personalizado
		productomod = ProductoAlmacenMod.objects.create(orden=orden, producto=producto, nombre=producto.nombre, codigo=producto.codigo, descripcion=producto.descripcion, categoria=producto.categoria, costo=producto.costo, precio_venta=producto.precio_venta, file=producto.file) 
		insumos = InsumoProducto.objects.filter(producto=producto)
		costos_especiales = CostoEspecial.objects.filter(producto=producto)

		for costo in costos_especiales:
			costomod = CostoEspecialAlmacen.objects.create(producto=productomod, concepto=costo.concepto, costo=costo.costo)

		for insumo in insumos:
			# crear insumo para producto duplicado
			insumomod = InsumoProductoMod.objects.create(insumo=insumo.insumo, producto=productomod, cantidad=insumo.cantidad, costototal=insumo.costototal)
			print insumomod
			# total_insumos_producto = insumo.cantidad * int(cantidad)
			# print total_insumos_producto
			# if total_insumos_producto <= insumo.insumo.stock:
			# 	print 'suficiente'
			# 	newstock = insumo.insumo.stock - total_insumos_producto
			# 	Insumo.objects.filter(pk=insumo.insumo.pk).update(stock=newstock)
			# 	post_save.send(Insumo, instance=insumo.insumo, created=False) #signal update costo stock
			# else:
			# 	newstock = insumo.insumo.stock - total_insumos_producto
			# 	Insumo.objects.filter(pk=insumo.insumo.pk).update(stock=newstock)
			# 	post_save.send(Insumo, instance=insumo.insumo, created=False) #signal update costo stock
			# 	print 'no alcanza'

		#print producto
		productoorden= ProductoOrdenAlmacen.objects.create(producto=productomod, orden=orden, unidad=unidad, cantidad=cantidad, color=color, comentario=comentario)
		print 'guardado'
		return HttpResponseRedirect(reverse('OrdenAlmacenDetail', args=(orden.id,)))
	return HttpResponse(template.render(context, request))




# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de orden > Detalle de producto

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def OrdenAlmacenProductoDetail(request, producto):
	current_user = request.user
	producto_orden = get_object_or_404(ProductoOrdenAlmacen, pk = producto)
	orden = get_object_or_404(OrdenAlmacen, pk = producto_orden.orden.id)
	insumos = InsumoProductoMod.objects.filter(producto=producto_orden.producto)
	checkinsumos = CheckInsumoProductoAlmacen.objects.filter(productorden=producto_orden)
	template =  get_template("detalle_producto_orden_almacen.html")
	pk = producto
	#form = OrdenProductoForm(initial={'orden':orden})
	#form.fields['orden'].widget = forms.HiddenInput()

	form1 = CostoEspecialAlmacenForm(initial={'producto':producto_orden.producto.pk})
	form1.fields['producto'].widget = forms.HiddenInput()
	if 'save' in request.POST:
		form1 = CostoEspecialAlmacenForm(request.POST)
		print request.POST
		if form1.is_valid():
			print 'valid'
			form1.save()
			return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto_orden.id,)))
		else:
			print 'error'
			print form1.errors, len(form1.errors)


	costoespeciales = CostoEspecialAlmacen.objects.filter(producto=producto_orden.producto)[:15]

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
			return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto_orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)

	print 'insumos'
	print insumos
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
		'pk':pk,'orden':orden, 'producto_orden':producto_orden, 'insumos':insumos, 'checkinsumos':checkinsumos, 'form1':form1, 'form':form, 'costoespeciales':costoespeciales,
	}
	
	return HttpResponse(template.render(context, request))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Asignar Material

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def ProductoInsumoAlmacen(request, productoalmacen):
	productoal =  get_object_or_404(ProductoOrdenAlmacen, pk = productoalmacen)
	producto = productoal.producto
	template =  get_template("producto_insumo_almacen.html")
	form = ProductoInsumoAlmacenForm(initial={'producto':producto})
	form.fields['producto'].widget = forms.HiddenInput()
	context = {
		'producto':producto,'form': form,
	}
	if request.method == 'POST':
	#if 'save' in request.POST:
		form = ProductoInsumoAlmacenForm(request.POST)
		if form.is_valid():
			
			cantidad = request.POST['cantidad']
			print cantidad
			insumopk = request.POST['insumo']
			insumo = get_object_or_404(Insumo, pk = insumopk) 
			print insumo
			insumoproducto= InsumoProductoMod.objects.create(insumo=insumo, producto=producto, cantidad=cantidad)
			print 'guardado'
			return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(productoal.id,)))
		else:
			print "Error en el form"
			print form.errors

	return HttpResponse(template.render(context, request))


from django.http import Http404  
# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Eliminar Material

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EliminarProductoInsumoAlmacen(request, pk, producto):
	productoal = get_object_or_404(ProductoOrdenAlmacen, pk = producto)
	producto = productoal.producto
	try:
		insumos = InsumoProductoMod.objects.get(pk=pk, producto=producto)
	except:
		raise Http404 
	else:
		
		insumos.delete()
		print 'insumo eliminado'
		return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(productoal.pk,)))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Editar Material
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EditarProductoInsumoAlmacen(request, pk, producto):
	
	post = get_object_or_404(InsumoProductoMod, pk=pk)
        if request.method == "POST":
            form = InsumoMod(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto,)))
        else:
            form = InsumoMod(instance=post)
        return render(request, 'editar_almacen_insumo.html', {'form': form})


# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Eliminar Costo Especial
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EliminarCostoEspecialAlmacen(request, pk, producto):
	try:
		insumos = CostoEspecialAlmacen.objects.get(pk=pk)
	except:
		#return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto,)))
		raise Http404 
	else:
		insumos.delete()
		print 'insumo eliminado'
		return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto,)))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Almacen > Detalle de producto > Editar Producto
@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def EditarProductoAlmacen(request, pk, producto):


	post = get_object_or_404(ProductoAlmacenMod, pk=pk)

	if 'save' in request.POST:
		form = ProductoMod(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save()
			post.save()
			#return redirect('listaProducto')
			return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(producto,)))
		else:
			print "Error en edición de producto"
			print form.errors
	else:
		form = ProductoMod(instance=post)

	form2 = productoaddcat()
	if 'save1' in request.POST:
		form2 = productoaddcat(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('EditarProductoAlmacen', args=(producto,pk)))
		else:
			print 'error'
			print form.errors, len(form.errors)
	else:
		form2 = productoaddcat()
	
	# post = get_object_or_404(ProductoAlmacenMod, pk=pk)
 #        if request.method == "POST":
 #            form = ProductoMod(request.POST, instance=post)
 #            if form.is_valid():
 #                post = form.save(commit=False)
 #                post.author = request.user
 #                post.save()
 #                return HttpResponseRedirect(reverse('OrdenAlmacenProductoDetail', args=(productos,)))
 #        else:
 #            form = ProductoMod(instance=post)
        return render(request, 'editar_almacen_producto.html', {'form': form, 'form2':form2, 'prod':producto})
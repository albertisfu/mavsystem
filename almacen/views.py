from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from forms import *
import django_filters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
# Vista Home
@login_required
def administradorHome(request):
	current_user = request.user
	template =  get_template("administrador.html")
	context = {
        'current_user': current_user,
    }
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Vista Alta insumos
@login_required
@group_required('Administrador', 'Produccion')
def administradorAlta(request):
	current_user = request.user
	template =  get_template("administradoralta.html")
	form = AltaForm()
	#context = {
	#	'current_user': current_user, 'form': form,
	#}
	if 'save' in request.POST:
		form = AltaForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save()
			post.save()
			return redirect('administradorInsumos')

	form2 = insumoaddcat()
	if 'save1' in request.POST:
		form2 = insumoaddcat(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('administradorAlta'))
		else:
			print 'error'
			print form.errors, len(form.errors)

	context = {
		'current_user': current_user, 'form': form, 'form2' : form2,
	}

	return HttpResponse(template.render(context, request))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > filtros lista de insumos

class InsumosFilter(django_filters.FilterSet):

	class Meta:
		model = Insumo
		fields = { #creamos los filtros necesarios 
        		  'categoria':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-stock', 'Menor Stock'),
				    ('stock', 'Mayor Stock'),

				)

# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > lista de insumos

@login_required
@group_required('Administrador', 'Produccion')
def administradorInsumos(request):
	current_user = request.user
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
	template =  get_template("administradorinsumos.html")
	context = {
		'current_user': current_user,'insumos': insumos,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > lista de insumos - busqueda

class InsumoListView(ListView):
	model = Insumo
	template_name = 'insumo_list.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion'))
	def dispatch(self, *args, **kwargs):
		return super(InsumoListView, self).dispatch(*args, **kwargs)
  

import operator
from django.db.models import Q
class SearchListView(InsumoListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(SearchListView, self).get_queryset()

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

# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo > Ver entradas - filtros lista de insumos

class EntradasFilter(django_filters.FilterSet):

	class Meta:
		model = Entrada
		fields = { #creamos los filtros necesarios 
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-fecha', 'Recientes'),
				    ('fecha', 'Antiguos'),

				)

# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo

@login_required
@group_required('Administrador', 'Produccion')
def adminInsumoDetail(request, insumo):
	insumo = get_object_or_404(Insumo, pk = insumo) 
	entradas = Entrada.objects.filter(insumo=insumo)
	salidas = Salida.objects.filter(insumo=insumo)
	template =  get_template("admininsumodetail.html")
	sort = request.GET.get('o') #orden del query filter
	if sort == None: #si no hay orden en URL se refiere a -fecha 
		sort = '-fecha'
	filters = EntradasFilter(request.GET, queryset=Entrada.objects.filter(insumo=insumo))
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		entradas= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		entradas = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		entradas = paginator.page(paginator.num_pages)


	context = {
        'insumo': insumo, 'entradas': entradas,'filters': filters,'sort':sort,
    }
	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo - Editar

@login_required
@group_required('Administrador', 'Produccion')
def editinsumo(request, pk):
    post = Insumo.objects.get(pk = pk)
    print post
    form = editinsumoform(instance=post)
    if request.method == 'POST':
       print request.POST
       post.nombre = request.POST.get('nombre')
       post.codigo = request.POST.get('codigo')
       post.descripcion = request.POST.get('descripcion')
       categoria = request.POST.get('categoria')
       category = Categoria.objects.get(pk = categoria)
       post.categoria = category 
       post.unidad = request.POST.get('unidad')
       post.costounitario = request.POST.get('costounitario')
       post.save()
       print 'save'
                             #payload = {'success': 'Concepto editado'}
                             #return HttpResponse(json.dumps(payload), content_type='application/json')
    else:
        form = editinsumoform(instance=post)
    return render(request, 'editinsumo.html', {'form': form, 'post':post})

# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo > Agregar entrada

@login_required
@group_required('Administrador', 'Produccion')
def adminInsumoEntrada(request, insumo):
	current_user = request.user
	insumo = get_object_or_404(Insumo, pk = insumo)
	template =  get_template("admininsumoentrada.html")
	form = EntradaForm(initial={'insumo':insumo, 'usuario':current_user})
	form.fields['insumo'].widget = forms.HiddenInput()
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['fecha'].widget = forms.HiddenInput()
	context = {
		'insumo':insumo,'form': form,
	}
	if 'save' in request.POST:
		
		form = EntradaForm(request.POST)
		cantidad = request.POST['cantidad']
		print cantidad
		if form.is_valid():
			
			form.save()
			#post.save() revisar en plataforma, se guarda 2 veces
			print 'guardado'
			return HttpResponseRedirect(reverse('adminInsumoDetail', args=(insumo.id,)))


	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo > Agregar salida

@login_required
@group_required('Administrador', 'Produccion')
def adminInsumoSalida(request, insumo):
	current_user = request.user
	insumo = get_object_or_404(Insumo, pk = insumo)
	template =  get_template("admininsumosalida.html")
	form = SalidaForm(initial={'insumo':insumo, 'usuario':current_user})
	form.fields['insumo'].widget = forms.HiddenInput()
	form.fields['usuario'].widget = forms.HiddenInput()
	form.fields['fecha'].widget = forms.HiddenInput()
	context = {
		'insumo':insumo,'form': form,
	}
	if 'save' in request.POST:
		
		form = SalidaForm(request.POST)
		if form.is_valid():
			
			form.save()
			#post.save() revisar en plataforma, se guarda 2 veces
			print 'guardado'
			return HttpResponseRedirect(reverse('adminInsumoDetail', args=(insumo.id,)))


	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo > Ver entradas

@login_required
@group_required('Administrador', 'Produccion')
def adminEntradas(request, insumo):
	insumo = get_object_or_404(Insumo, pk = insumo) 
	entradas = Entrada.objects.filter(insumo=insumo)
	template =  get_template("adminlistaentradas.html")
	sort = request.GET.get('o') #orden del query filter
	if sort == None: #si no hay orden en URL se refiere a -fecha 
		sort = '-fecha'
	filters = EntradasFilter(request.GET, queryset=Entrada.objects.filter(insumo=insumo))
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		entradas= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		entradas = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		entradas = paginator.page(paginator.num_pages)


	context = {
        'insumo': insumo, 'entradas': entradas,'filters': filters,'sort':sort,
    }
	return HttpResponse(template.render(context, request))



# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo > Ver salidas - filtros lista de insumos

class SalidasFilter(django_filters.FilterSet):

	class Meta:
		model = Salida
		fields = { #creamos los filtros necesarios 
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-fecha', 'Recientes'),
				    ('fecha', 'Antiguos'),

				)



# ---------------------------------------------------------
# ---------------------------------------------------------
# Inventario > Detalle insumo > Ver salidas

@login_required
@group_required('Administrador', 'Produccion')
def adminSalidas(request, insumo):
	insumo = get_object_or_404(Insumo, pk = insumo) 
	salidas = Salida.objects.filter(insumo=insumo)
	template =  get_template("adminlistasalidas.html")
	sort = request.GET.get('o') #orden del query filter
	if sort == None: #si no hay orden en URL se refiere a -fecha 
		sort = '-fecha'
	filters = SalidasFilter(request.GET, queryset=Salida.objects.filter(insumo=insumo))
	paginator = Paginator(filters, 10)
	page = request.GET.get('page')
	try:
		salidas= paginator.page(page)
	except PageNotAnInteger:
        # Si la pagina no es un entero muestra la primera pagina
		salidas = paginator.page(1)
	except EmptyPage:
        # si la pagina esta fuera de rango, muestra la ultima pagina
		salidas = paginator.page(paginator.num_pages)


	context = {
        'insumo': insumo, 'salidas': salidas,'filters': filters,'sort':sort,
    }
	return HttpResponse(template.render(context, request))


# ---------------------------------------------------------
# ---------------------------------------------------------
#Vistas Orden Compra


@login_required
@group_required('Administrador', 'Produccion')
def AddOrdenCompra(request):
	current_user = request.user
	template =  get_template("add_orden_compra.html")
	form = OrdenForm()
	#context = {
	#	'current_user': current_user, 'form': form,
	#}
	if 'save' in request.POST:
		form = OrdenForm(request.POST)
		if form.is_valid():
			post = form.save()
			post.save()
			return redirect('administradorInsumos')

	form2 = ProveeForm()
	if 'save1' in request.POST:
		form2 = ProveeForm(request.POST)
		
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('AddOrdenCompra'))
		else:
			print 'error'
			print form.errors, len(form.errors)

	context = {
		'current_user': current_user, 'form': form, 'form2' : form2,
	}

	return HttpResponse(template.render(context, request))

# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista ordenes Compra - filtros

class OrdenesCompraFilter(django_filters.FilterSet):
	class Meta:
		model = OrdenCompra
		fields = { #creamos los filtros necesarios 
        		  'estatus':['exact'],
        		 }
		order_by = (#definimos los terminos de orden y su alias, se coloca un - para indicar orden descendente
				    ('-fecha', 'Fecha menor'),
				    ('fecha', 'Fecha mayor'),
				    )

		

# ---------------------------------------------------------
# ---------------------------------------------------------
# /administrador/lista_ordenes_compra

@login_required
@group_required('Administrador', 'Produccion')
def listaOrdenesCompra(request):
	filters = OrdenesCompraFilter(request.GET, queryset=OrdenCompra.objects.all()) 
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
	template =  get_template("listaordenescompra.html")
	context = {
		'ordenes': ordenes,'filters': filters,
	}
	
	return HttpResponse(template.render(context, request))




# ---------------------------------------------------------
# ---------------------------------------------------------
# Ordenes > Lista de ordenes > buscador


class OrdenesCompraListView(ListView):
	model = OrdenCompra
	template_name = 'ordenes_compra_list.html'

	@method_decorator(login_required)
	@method_decorator(group_required('Administrador', 'Produccion'))
	def dispatch(self, *args, **kwargs):
		return super(OrdenesCompraListView, self).dispatch(*args, **kwargs)
  

import operator
from django.db.models import Q
class SearchOrdenesCompraListView(OrdenesCompraListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(SearchOrdenesCompraListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(proveedor__nombre__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(numero__icontains=q) for q in query_list))|
                reduce(operator.and_,
                       (Q(orden__codigo__icontains=q) for q in query_list))
            )

        return result


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Ver a detalle de orden de compra

@login_required
@group_required('Administrador', 'Produccion')
def OrdenCompraDetalle(request, pk):
	#paginate_by = 2 # Elementos por pagina
	orden = get_object_or_404(OrdenCompra, pk = pk)
	form2 = addinsumo(initial={'orden':orden})
	form2.fields['orden'].widget = forms.HiddenInput()
	if 'save1' in request.POST:
		form2 = addinsumo(request.POST)
		print request.POST
		if form2.is_valid():
			print 'valid'
			form2.save()
			return HttpResponseRedirect(reverse('OrdenCompraDetalle', args=(orden.id,)))
		else:
			print 'error'
			print form.errors, len(form.errors)
	insumos = OrdenConcepto.objects.filter(orden=orden.id)

	if 'cancel' in request.POST: #cancel order
		orden.estatus = 4
		orden.save()

	if 'confirmar' in request.POST: #cancel order
		print 'confirmar'
		orden.estatus = 2
		orden.save()
	print request.POST



	if 'conceptos' in request.POST:
		data = request.POST.copy()
		conceptos = request.POST.get('conceptos')
		if not conceptos:
			conceptoslist = []
		else:
			conceptoslist = conceptos.split(",")

		if len(conceptoslist)>0:
			conceptos = []
 			for concepto in conceptoslist:
				if concepto != '':
					concept = get_object_or_404(OrdenConcepto, pk = int(concepto))
					OrdenConcepto.objects.filter(pk = int(concepto)).update(recibido=True)
					insumo = Insumo.objects.get(pk=concept.insumo.pk)
					print insumo
					print insumo.stock
					currentstock = insumo.stock
					print currentstock
					newstock = currentstock + concept.cantidad
					print newstock
					costostock = insumo.costounitario * newstock
					Insumo.objects.filter(pk=concept.insumo.pk).update(stock=newstock, costostock=costostock)
                  
				
	return render(request, 'orden_compra_detalle.html', {'orden': orden, 'form2':form2, 'insumos':insumos})

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Impresion orden de compra

@login_required
@group_required('Administrador', 'Produccion', 'Ventas')
def orden_compra_impresion(request, pk):
	orden = get_object_or_404(OrdenCompra, pk = pk) 
	insumos = OrdenConcepto.objects.filter(orden=orden.id)
	contexto = {'orden':orden,'insumos':insumos}
	template = get_template('imprimir_orden_compra.html')
	rendered_html = template.render(contexto).encode(encoding="ISO-8859-1")
	pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  '/css/pdf.css')])
	http_response = HttpResponse(rendered_html, content_type='text/html')
	return http_response 

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Editar concepto
@login_required
@group_required('Administrador', 'Produccion')
def editarconceptocobro(request, pk):
    if request.method == 'POST':
       post = OrdenConcepto.objects.get(pk = pk)
       formy = editinsumocompra(instance=post)
       #print request.POST
       #post.producto = request.POST.get('producto')
       #post.orden = request.POST.get('orden')
       #print request.POST.get('cantidad')
       post.cantidad = float(request.POST.get('cantidad'))
       post.save()
       return HttpResponseRedirect(reverse('OrdenCompraDetalle', args=(post.orden.id,)))

       #print 'save'
                             #payload = {'success': 'Concepto editado'}
                             #return HttpResponse(json.dumps(payload), content_type='application/json')
    else:
        post = OrdenConcepto.objects.get(pk = pk)
        formy = editinsumocompra(instance=post)
        formy.fields['orden'].widget = forms.HiddenInput()
       
        return render(request, 'edit_concepto_compra.html', {'formy': formy, 'post':post})




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import json
@login_required
@group_required('Administrador', 'Produccion')
def deleteconceptocobro(request, pk):    
    con = OrdenConcepto.objects.get(pk = pk)
    
    con.delete()
    payload = {'success': 'Concepto eliminado'}
    return HttpResponse(json.dumps(payload), content_type='application/json')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Modificar orden

@login_required
@group_required('Administrador', 'Produccion')
def modificar_orden_compra(request, pk):
	if request.method == "POST":
		print 'post'
		post = get_object_or_404(OrdenCompra, pk=pk)

		postan = get_object_or_404(OrdenCompra, pk=pk)
		#print post
		form = OrdenCompraModificar(request.POST, instance=post)
		#print form
		if form.is_valid():
			print 'valid'
			#post_save.disconnect(orden_uid, sender=OrdenCompra)
			post = form.save(commit=False)
            #post.clave = post.clave_doc + '-' + str(pk) + '-' + str(post.rev_id)
			#ordercount = Alta_orden.objects.filter(preclave=post.preclave).count() + 1
			#post.clave = post.preclave + str(ordercount)			
			#post.ordencobro = post.ordencobro
			#print post.ordencobro
			post.usuario = request.user
			post.save()
			#post_save.connect(orden_uid, sender=Alta_orden)
            #form.save_m2m() #para guardar los datos del manytomany
			payload = {'success': 1, 'ido': post.id}
			return HttpResponse(json.dumps(payload), content_type='application/json')  
			#return redirect('ver_ordenes_entrada')#cambiar esta redireccion por js por que al ser modal solo carga internamente


	else: 
		post = get_object_or_404(OrdenCompra, pk=pk)
		form = OrdenCompraModificar(instance=post)
		form.fields['orden'].widget = forms.HiddenInput()
		form.fields['fecha'].widget = forms.HiddenInput()
		form.fields['numero'].widget = forms.HiddenInput()
		return render(request, 'edit_order_compra.html', {'form': form, 'post':post})



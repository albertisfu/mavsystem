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



from django.conf.urls import patterns, include, url
import almacen.views
from views import SearchListView, InsumoListView
urlpatterns = [

    url(r'^administrador/$', almacen.views.administradorHome, name='administradorHome'), 
   	url(r'^administrador/alta$', almacen.views.administradorAlta, name='administradorAlta'), 
   	url(r'^administrador/insumos$', almacen.views.administradorInsumos, name='administradorInsumos'), 
   	url(r'^administrador/lista_insumos$', InsumoListView.as_view(), name='insumo-list'),
   	url(r'^administrador/search/$', SearchListView.as_view(), name='search_url'),
   	url(r'^administrador/insumo/(?P<insumo>[-\w]+)/$', 'almacen.views.adminInsumoDetail', name='adminInsumoDetail'), 
   	url(r'^administrador/entrada/(?P<insumo>[-\w]+)/$', 'almacen.views.adminInsumoEntrada', name='adminInsumoEntrada'),
   	url(r'^administrador/salida/(?P<insumo>[-\w]+)/$', 'almacen.views.adminInsumoSalida', name='adminInsumoSalida'), 
   	url(r'^administrador/entradas/(?P<insumo>[-\w]+)/$', 'almacen.views.adminEntradas', name='adminEntradas'),
   	url(r'^administrador/salidas/(?P<insumo>[-\w]+)/$', 'almacen.views.adminSalidas', name='adminSalidas'),  
   ]


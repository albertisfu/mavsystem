from django.conf.urls import patterns, include, url
from almacen import views as almacen_views
from views import SearchListView, InsumoListView
urlpatterns = [

    url(r'^administrador/$', almacen_views.administradorHome, name='administradorHome'), 
   	url(r'^administrador/alta$', almacen_views.administradorAlta, name='administradorAlta'), 
   	url(r'^administrador/insumos$', almacen_views.administradorInsumos, name='administradorInsumos'), 
   	url(r'^administrador/lista_insumos$', InsumoListView.as_view(), name='insumo-list'),
   	url(r'^administrador/search/$', SearchListView.as_view(), name='search_url'),
   	url(r'^administrador/insumo/(?P<insumo>[-\w]+)/$', almacen_views.adminInsumoDetail, name='adminInsumoDetail'), 
   	url(r'^administrador/entrada/(?P<insumo>[-\w]+)/$', almacen_views.adminInsumoEntrada, name='adminInsumoEntrada'),
   	url(r'^administrador/salida/(?P<insumo>[-\w]+)/$', almacen_views.adminInsumoSalida, name='adminInsumoSalida'), 
   	url(r'^administrador/entradas/(?P<insumo>[-\w]+)/$', almacen_views.adminEntradas, name='adminEntradas'),
   	url(r'^administrador/salidas/(?P<insumo>[-\w]+)/$', almacen_views.adminSalidas, name='adminSalidas'),  
      url(r'^administrador/edit_insumo/(?P<pk>[0-9]+)/$', almacen_views.editinsumo, name='editinsumo'),
   ]


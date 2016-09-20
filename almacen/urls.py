from django.conf.urls import patterns, include, url
from almacen import views as almacen_views
from views import SearchListView, InsumoListView, OrdenesCompraListView, SearchOrdenesCompraListView
urlpatterns = [

    url(r'^$', almacen_views.administradorHome, name='administradorHome'), 
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

      url(r'^administrador/add_orden_compra$', almacen_views.AddOrdenCompra, name='AddOrdenCompra'), 
      url(r'^administrador/lista_ordenes_compra$', almacen_views.listaOrdenesCompra, name='listaOrdenesCompra'),
      url(r'^administrador/orden_compra_detalle/(?P<pk>[-\w]+)/$', almacen_views.OrdenCompraDetalle, name='OrdenCompraDetalle'),
      url(r'^administrador/orden_compra_detalle/imprimir/(?P<pk>[-\w]+)/$', almacen_views.orden_compra_impresion, name='orden_compra_impresion'), 

      url(r'^administrador/modificar_orden_compra/(?P<pk>[-\w]+)/$', almacen_views.modificar_orden_compra, name='modificar_orden_compra'), 
       url(r'^administrador/editarconceptocobro/(?P<pk>[-\w]+)/$', almacen_views.editarconceptocobro, name='editarconceptocobro'), 
        url(r'^administrador/deleteconceptocobro/(?P<pk>[-\w]+)/$', almacen_views.deleteconceptocobro, name='deleteconceptocobro'), 
      
      #search Orders
    url(r'^administrador/ordenes_compra_lista$', OrdenesCompraListView.as_view(), name='search-orders_compra'),
      url(r'^administrador/search_orden_compra/$', SearchOrdenesCompraListView.as_view(), name='search_orden_compra'),

      url(r'', include ('panel.urls')),
   ]


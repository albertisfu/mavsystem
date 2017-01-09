from django.conf.urls import patterns, include, url
from produccion import views as produccion_views
from views import SearchPopListView, InsumoPopListView, OrdenesListView, SearchOrdenesListView, ProductoPopListView, SearchProductoPopListView, SearchClientesListView, ClientesListView, CotizacionesListView, SearchCotizacionesListView, listaOrdenesAlmacen

urlpatterns = [

   	url(r'^administrador/producto/alta-producto$', produccion_views.altaProducto, name='altaProducto'), 
   	url(r'^administrador/producto/lista-productos$', produccion_views.listaProducto, name='listaProducto'), 
   	url(r'^administrador/producto/(?P<producto>[-\w]+)/$', produccion_views.ProductoDetail, name='ProductoDetail'), 
   	url(r'^administrador/producto/asignar-insumo/(?P<producto>[-\w]+)/$', produccion_views.ProductoInsumo, name='ProductoInsumo'),
   	url(r'^administrador/pop_insumolist$', InsumoPopListView.as_view(), name='insumopop_list'),
   	url(r'^administrador/popsearch/$', SearchPopListView.as_view(), name='searchpop_url'),
   	url(r'^administrador/popinsumo$', produccion_views.popInsumo, name='popInsumo'), 
   	#url(r'^administrador/salidas/(?P<insumo>[-\w]+)/', 'almacen.views.adminSalidas', name='adminSalidas'),  

		# ajax
	 	url(r'^administrador/insumo_ajax$', produccion_views.ajaxInsumo, name='ajaxInsumo'), 
	 	url(r'^administrador/producto_ajax$', produccion_views.ajaxProducto, name='ajaxProducto'), 

    # ordenes 
    url(r'^administrador/orden/alta-orden$', produccion_views.altaOrden, name='altaOrden'), 
    url(r'^administrador/orden/lista-ordenes$', produccion_views.listaOrdenes, name='listaOrdenes'), 
    url(r'^administrador/orden/detalle/(?P<orden>[-\w]+)/$', produccion_views.OrdenDetail, name='OrdenDetail'),
    url(r'^administrador/orden/imprimir/(?P<orden>[-\w]+)/$', produccion_views.orden_impresion, name='orden_impresion'), 
    url(r'^administrador/orden/asignar-producto/(?P<orden>[-\w]+)/$', produccion_views.OrdenProducto, name='OrdenProducto'),
    url(r'^administrador/orden/producto-orden/(?P<producto>[-\w]+)/$', produccion_views.OrdenProductoDetail, name='OrdenProductoDetail'),
    url(r'^administrador/checkinsumos/(?P<orden>[-\w]+)/(?P<insumo>[-\w]+)$', produccion_views.HistoryCheckInsumo, name='HistoryCheckInsumo'),

    url(r'^administrador/pop_product_list$', ProductoPopListView.as_view(), name='producto_pop_list'),
    url(r'^administrador/popsearch_product/$', SearchProductoPopListView.as_view(), name='searchpop_producto_url'),
    url(r'^administrador/pop_product$', produccion_views.popProducto, name='popProduct'), 


    # search Orders
    url(r'^administrador/ordenes_lista$', OrdenesListView.as_view(), name='search-orders'),
   	url(r'^administrador/buscar/orden/$', SearchOrdenesListView.as_view(), name='search_orden_url'),

    # Cotizaciones
    url(r'^administrador/cotizacion/alta-cotizacion$', produccion_views.altaCotizacion, name='altaCotizacion'),
    url(r'^administrador/cotizacion/lista-cotizaciones$', produccion_views.listaCotizaciones, name='listaCotizaciones'), 
    url(r'^administrador/cotizacion/(?P<orden>[-\w]+)/$', produccion_views.CotizacionDetail, name='CotizacionDetail'),
    url(r'^administrador/cotizacion/asignar-producto/(?P<orden>[-\w]+)/$', produccion_views.CotizacionProducto, name='CotizacionProducto'),
    url(r'^administrador/cotizacion/productos-cotizacion/(?P<producto>[-\w]+)/$', produccion_views.CotizacionProductoDetail, name='CotizacionProductoDetail'),
    url(r'^administrador/cotizacion/imprimir/(?P<orden>[-\w]+)/$', produccion_views.cotizacion_impresion, name='cotizacion_impresion'),

    # Almacen
    url(r'^administrador/almacen/alta-orden$', produccion_views.altaOrdenAlmacen, name='altaOrdenAlmacen'),
    url(r'^administrador/almacen/lista-ordenes$', produccion_views.listaOrdenesAlmacen, name='listaOrdenesAlmacen'),
    url(r'^administrador/almacen/detalle/(?P<orden>[-\w]+)/$', produccion_views.OrdenAlmacenDetail, name='OrdenAlmacenDetail'), 
    url(r'^administrador/almacen/asignar-producto/(?P<orden>[-\w]+)/$', produccion_views.OrdenAlmacenProducto, name='OrdenAlmacenProducto'),
    url(r'^administrador/almacen/producto-orden/(?P<producto>[-\w]+)/$', produccion_views.OrdenAlmacenProductoDetail, name='OrdenAlmacenProductoDetail'),

    # Almacen producto personalizado

    url(r'^administrador/almacen/producto/asignar-insumo/(?P<productoalmacen>[-\w]+)/$', produccion_views.ProductoInsumoAlmacen, name='ProductoInsumoAlmacen'),
    url(r'^administrador/almacen/producto/eliminar-insumo/(?P<insumo>[-\w]+)/$', produccion_views.EliminarProductoInsumoAlmacen, name='EliminarProductoInsumoAlmacen'),

    # Buscar cotizaciones
    url(r'^administrador/cotizaciones_lista$', CotizacionesListView.as_view(), name='search-orders'),
    url(r'^administrador/buscar/cotizacion/$', SearchCotizacionesListView.as_view(), name='search_cotizacion_url'),

		# clientes
		url(r'^administrador/lista-clientes$', produccion_views.listaClientes, name='listaClientes'),
		url(r'^administrador/alta-cliente$', produccion_views.altaCliente, name='altaCliente'),  

		# search Clientes
    url(r'^administrador/clientes_lista$', ClientesListView.as_view(), name='search-clientes'),
    url(r'^administrador/search_cliente/$', SearchClientesListView.as_view(), name='search_cliente_url'),
    url(r'^administrador/cliente/(?P<cliente>[-\w]+)/$', produccion_views.ClienteDetail, name='ClienteDetail'), 


   ]


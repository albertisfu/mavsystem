from django.conf.urls import patterns, include, url
from produccion import views as produccion_views
from views import SearchPopListView, InsumoPopListView, OrdenesListView, SearchOrdenesListView, ProductoPopListView, SearchProductoPopListView

urlpatterns = [

   
   	url(r'^administrador/alta_producto$', produccion_views.altaProducto, name='altaProducto'), 
   	url(r'^administrador/lista_productos$', produccion_views.listaProducto, name='listaProducto'), 
   	url(r'^administrador/producto/(?P<producto>[-\w]+)/$', produccion_views.ProductoDetail, name='ProductoDetail'), 
   	url(r'^administrador/asignar_insumo/(?P<producto>[-\w]+)/$', produccion_views.ProductoInsumo, name='ProductoInsumo'),
   	url(r'^administrador/pop_insumolist$', InsumoPopListView.as_view(), name='insumopop_list'),
   	url(r'^administrador/popsearch/$', SearchPopListView.as_view(), name='searchpop_url'),
   	url(r'^administrador/popinsumo$', produccion_views.popInsumo, name='popInsumo'), 
   	#url(r'^administrador/salidas/(?P<insumo>[-\w]+)/', 'almacen.views.adminSalidas', name='adminSalidas'),  


      #ordenes 

    url(r'^administrador/alta_orden$', produccion_views.altaOrden, name='altaOrden'), 
    url(r'^administrador/lista_ordenes$', produccion_views.listaOrdenes, name='listaOrdenes'), 
    url(r'^administrador/orden/(?P<orden>[-\w]+)/$', produccion_views.OrdenDetail, name='OrdenDetail'), 
    url(r'^administrador/asignar_producto/(?P<orden>[-\w]+)/$', produccion_views.OrdenProducto, name='OrdenProducto'),
    url(r'^administrador/producto_orden/(?P<producto>[-\w]+)/$', produccion_views.OrdenProductoDetail, name='OrdenProductoDetail'), 
    url(r'^administrador/checkinsumos/(?P<orden>[-\w]+)/(?P<insumo>[-\w]+)$', produccion_views.HistoryCheckInsumo, name='HistoryCheckInsumo'),

    url(r'^administrador/pop_product_list$', ProductoPopListView.as_view(), name='producto_pop_list'),
    url(r'^administrador/popsearch_product/$', SearchProductoPopListView.as_view(), name='searchpop_producto_url'),
    url(r'^administrador/pop_product$', produccion_views.popProducto, name='popProduct'), 


    #search Orders
    url(r'^administrador/ordenes_lista$', OrdenesListView.as_view(), name='search-orders'),
   	url(r'^administrador/search_orden/$', SearchOrdenesListView.as_view(), name='search_orden_url'),


   ]


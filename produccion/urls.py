from django.conf.urls import patterns, include, url
import produccion.views
urlpatterns = [

   
   	url(r'^administrador/alta_producto$', produccion.views.altaProducto, name='altaProducto'), 
   	url(r'^administrador/lista_productos$', produccion.views.listaProducto, name='listaProducto'), 
   	url(r'^administrador/producto/(?P<producto>\w+)/', produccion.views.ProductoDetail, name='ProductoDetail'), 
   	url(r'^administrador/asignar_insumo/(?P<producto>\w+)/', produccion.views.ProductoInsumo, name='ProductoInsumo'),

   	#url(r'^administrador/salidas/(?P<insumo>\w+)/', 'almacen.views.adminSalidas', name='adminSalidas'),  
   ]


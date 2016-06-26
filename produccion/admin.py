from django.contrib import admin

# Register your models here.
from models import Cliente, Categoria, Producto, InsumoProducto, Orden, ProductoOrden, ComentariosOrden

class CategoriaAdmin(admin.ModelAdmin):
    model = Categoria

class InsumoProductoAdmin(admin.ModelAdmin):
    model = InsumoProducto


class ClienteAdmin(admin.ModelAdmin):
    model = Cliente


class ProductoAdmin(admin.ModelAdmin):
    model = Producto


class OrdenAdmin(admin.ModelAdmin):
    model = Orden


class ProductoOrdenAdmin(admin.ModelAdmin):
    model = ProductoOrden

class ComentariosOrdenAdmin(admin.ModelAdmin):
    model = ProductoOrden

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(InsumoProducto, InsumoProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(ProductoOrden, ProductoOrdenAdmin)
admin.site.register(ComentariosOrden, ComentariosOrdenAdmin)
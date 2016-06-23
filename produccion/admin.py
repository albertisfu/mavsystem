from django.contrib import admin

# Register your models here.
from models import Cliente, Categoria, Producto, InsumoProducto

class CategoriaAdmin(admin.ModelAdmin):
    model = Categoria

class InsumoProductoAdmin(admin.ModelAdmin):
    model = InsumoProducto


class ClienteAdmin(admin.ModelAdmin):
    model = Cliente


class ProductoAdmin(admin.ModelAdmin):
    model = Producto

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(InsumoProducto, InsumoProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
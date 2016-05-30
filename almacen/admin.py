from django.contrib import admin

from models import Insumo, Categoria, Entrada, Salida
# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    model = Categoria


class InsumoAdmin(admin.ModelAdmin):
    model = Insumo

"""class StockAdmin(admin.ModelAdmin):
    model = Stock
"""

class EntradaAdmin(admin.ModelAdmin):
    model = Entrada


class SalidaAdmin(admin.ModelAdmin):
    model = Salida


admin.site.register(Insumo, InsumoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
"""admin.site.register(Stock, StockAdmin)"""
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Salida, SalidaAdmin)
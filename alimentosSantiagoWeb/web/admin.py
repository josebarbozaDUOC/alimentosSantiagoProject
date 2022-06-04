from django.contrib import admin
from .models import Restaurant, Producto, Tipo_producto, Tipo_menu, Avatar, Tipo_pago, Envio

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre","precio","restaurant"]
    list_editable = ["precio"]
    search_fields = ["nombre"]
    list_filter = ["restaurant", "tipo_producto"]
    list_per_page = 12

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]
    list_per_page = 12

class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]
    list_per_page = 12
    
class TipoMenuAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]
    list_per_page = 12

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Tipo_producto, TipoProductoAdmin)
admin.site.register(Tipo_menu, TipoMenuAdmin)
admin.site.register(Envio)
admin.site.register(Tipo_pago)
admin.site.register(Avatar)
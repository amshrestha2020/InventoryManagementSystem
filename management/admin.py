from django.contrib import admin
from management.models import Vendor, Unit, Customer, Inventory

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Unit)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile']
    search_fields = ['name', 'mobile']
admin.site.register(Customer, CustomerAdmin)


class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__unit__title']
    list_display = ['product', 'purchase_quantity', 'sale_quantity', 
    'total_balance_quantity', 'product_unit', 'purchase_date', 
    'sale_date', 'customer']
admin.site.register(Inventory, InventoryAdmin)
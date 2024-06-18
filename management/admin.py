from django.contrib import admin
from management.models import Vendor, Unit, Product, Customer, Purchase, Sale, Inventory

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Unit)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile']
    search_fields = ['name', 'mobile']
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit']
    search_fields = ['title', 'unit__title']
admin.site.register(Product, ProductAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'quantity', 'price', 
    'vendor', 'purchase_date']
    search_fields = ['product__title']
admin.site.register(Purchase, PurchaseAdmin)

class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'price', 
    'total_amount', 'sale_date']
    search_fields = ['product__title']
admin.site.register(Sale, SaleAdmin)

class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__unit__title']
    list_display = ['product', 'purchase_quantity', 'sale_quantity', 
    'total_balance_quantity', 'product_unit', 'purchase_date', 
    'sale_date', 'vendor', 'customer']
admin.site.register(Inventory, InventoryAdmin)
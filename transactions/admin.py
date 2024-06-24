from django.contrib import admin

# Register your models here.
from transactions.models import Sale, Purchase

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ('item', 'customer_name','payment_method', 'quantity', 'price', 'amount_received')
    list_display = ('item', 'slug', 'customer_name', 'transaction_date', 'payment_method', 'quantity', 'price', 'total_value', 'amount_received', 'balance', 'profile')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    fields = ('item', 'description', 'order_date', 'delivery_date', 'quantity', 'price', 'delivery_status')
    list_display = ('item', 'order_date', 'delivery_date', 'quantity', 'delivery_status', 'price', 'total_value')
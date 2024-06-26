# tutorial/tables.py
import django_tables2 as tables
from store.models import Item, Delivery
from django.shortcuts import render

class ItemTable(tables.Table):
    class Meta:
        model = Item
        template_name = "django_tables2/semantic.html"
        fields = ('id', 'item_name','item_category', 'price', 'item_image', 'description')
        order_by_field = 'sort'

class DeliveryTable(tables.Table):
    class Meta:
        model = Delivery
        fields = ('id', 'item', 'customer_name', 'phone_number', 'location', 'date','is_delivered')
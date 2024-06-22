from django.contrib import admin

# Register your models here.
from store.models import Category, Delivery, Item, Cart


admin.site.register(Category)
admin.site.register(Delivery)
admin.site.register(Cart)
admin.site.register(Item)
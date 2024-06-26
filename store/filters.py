import django_filters
from store.models import Item

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ['item_name', 'item_category']
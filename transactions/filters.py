import django_filters
from transactions.models import Sale, Purchase

class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['item', 'transaction_date', 'profile']

class PurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = Purchase
        fields = ['item', 'delivery_status']
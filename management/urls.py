from django.urls import path
from .views import dashboard, VendorListView, vendor_edit, vendor_delete, CustomerListView, customer_edit, customer_delete, ItemSearchListView, VendorCreateView

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('vendor/', VendorListView.as_view(), name='vendor'),
    path('vendors/', VendorCreateView.as_view(), name='vendor_create'),
    path('vendor/<int:pk>/edit/', vendor_edit, name='vendor_edit'),
    path('vendor/<int:pk>/delete/', vendor_delete, name='vendor_delete'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/edit/', customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', customer_delete, name='customer_delete'),
    path('customer_search/',ItemSearchListView.as_view(), name="customer_search"),


]
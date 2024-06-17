from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    PurchaseListView,
    PurchaseDetailView,
    PurchaseCreateView,
    PurchaseUpdateView,
    PurchaseDeleteView,
    SaleListView,
    SaleDetailView,
    SaleCreateView,
    SaleUpdateView,
    SaleDeleteView,
)

urlpatterns = [
    path('purchases/', PurchaseListView.as_view(), name="purchase_list"),
    path('purchase/<slug:slug>/', PurchaseDetailView.as_view(), name='purchase_detail'),
    path('new-purchase/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/<int:pk>/update/', PurchaseUpdateView.as_view(), name='purchase_update'),
    path('purchase/<int:pk>/delete/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    path('sales/',SaleListView.as_view(), name="sales_list"),
    path('sale/<int:pk>/', SaleDetailView.as_view(), name='sales_detail'),
    path('new-sale/', SaleCreateView.as_view(), name='sales_create'),
    path('sale/<slug:slug>/update/', SaleUpdateView.as_view(), name='sales_update'),
    path('sale/<slug:slug>/delete/', SaleDeleteView.as_view(), name='sales_delete'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
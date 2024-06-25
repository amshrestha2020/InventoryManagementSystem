from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ItemSearchListView,
    DeliveryListView,
    DeliveryDetailView,
    DeliveryCreateView,
    DeliveryUpdateView,
    DeliveryDeleteView,

)

from accounts.views import ColorsView


urlpatterns = [
    path('product/',ProductListView.as_view(), name="products_list"),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='products_detail'),
    path('new-product/', ProductCreateView.as_view(), name='products_create'),
    path('product/<slug:slug>/update/', ProductUpdateView.as_view(), name='products_update'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='products_delete'),
    path('search/',ItemSearchListView.as_view(), name="item_search_list_view"),

    path('deliveries/',DeliveryListView.as_view(), name="deliveries"),
    path('delivery/<slug:slug>/', DeliveryDetailView.as_view(), name='delivery_detail'),
    path('new-delivery/', DeliveryCreateView.as_view(), name='delivery_create'),
    path('delivery/<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery_update'),
    path('delivery/<int:pk>/delete/', DeliveryDeleteView.as_view(), name='delivery_delete'),

    # homepage_userside
    path('colors/', ColorsView.as_view(), name='colors'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
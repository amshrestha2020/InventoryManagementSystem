from django.urls import path
from .views import (  
                    AboutUsView, 
                    SearchAutoView, 
                    SearchView, 
                    AjaxColorView, 
                    FaqView, 
                    OrderSummary, )

app_name = 'homepage'

urlpatterns = [
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('search/', SearchView.as_view(), name='search'),
    path('search_auto/', SearchAutoView.as_view(), name='search_auto'),

    # path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('ajaxcolor/', AjaxColorView.as_view(), name='ajaxcolor'),
    path('faq/', FaqView.as_view(), name='faq'),
    
    path('order_summary/', OrderSummary.as_view(), name='order_summary'),
]

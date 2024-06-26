from django.urls import path
from .views import (  
                    AboutUsView, 
                    SearchAutoView, 
                    SearchView, 
                    AjaxColorView, 
                    FaqView,
                    AddToCartView,
                    add_to_cart,
                    remove_from_the_cart,
                    remove_single_from_the_cart )

app_name = 'homepage'

urlpatterns = [
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('search/', SearchView.as_view(), name='search'),
    path('search_auto/', SearchAutoView.as_view(), name='search_auto'),

    path('ajaxcolor/', AjaxColorView.as_view(), name='ajaxcolor'),
    path('faq/', FaqView.as_view(), name='faq'),
    
]

from django.urls import path
from .views import ( SelectLanguageView, 
                    AboutUsView, 
                    SearchAutoView, 
                    SearchView, 
                    ProductDetailView, 
                    AjaxColorView, 
                    FaqView, 
                    SelectCurrencyView, 
                    SaveLangCurView,
                    IndexView,
                    ProductListView,
                    SortedProductListView,
                    UserSortedProductListView,
                    UserProductListView, )


urlpatterns = [
    path('selectlanguage/', SelectLanguageView.as_view(), name='selectlanguage'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('search/', SearchView.as_view(), name='search'),
    path('search_auto/', SearchAutoView.as_view(), name='search_auto'),

    path('product/<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('ajaxcolor/', AjaxColorView.as_view(), name='ajaxcolor'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('selectcurrency/', SelectCurrencyView.as_view(), name='selectcurrency'),
    path('savelangcur/', SaveLangCurView.as_view(), name='savelangcur'),
    
    path('products/', UserProductListView, name = 'productlist'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('sortedproducts/<str:keyword>/', SortedProductListView.as_view(), name='sorted_product_list'),
    path('usersortedproducts/<str:keyword>/', UserSortedProductListView.as_view(), name='user_sorted_product_list'),

]

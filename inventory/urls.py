"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from homepage.views import ( 
                    DashboardView, 
                    ProductListView,)
from django.conf.urls.static import static

from homepage.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include('management.urls')),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('transactions/', include('transactions.urls')),
    path('bills/', include('bills.urls')),
    path('invoice/', include('invoice.urls')),
    # path('', auth_views.LoginView.as_view(template_name='login.html'), name='user_login'),

    path('admin_dashboard/', DashboardView.as_view(), name='admin_dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('', Base, name='base'),
    path('', ProductListView.as_view(), name='items'),
    path('item_list/<category_name>/', HomeView.as_view(), name='item_list_by_category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('order_summary/', OrderSummary.as_view(), name='order_summary'),
	
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_the_cart/<slug>/', remove_from_the_cart, name='remove_from_the_cart'),
    path('remove_single_from_the_cart/<slug>/', remove_single_from_the_cart, name='remove_single_from_the_cart'),
    

    path('checkout/', CheckoutView.as_view(), name='checkout'),
	path('add_coupon/', AddCouponView.as_view(), name="add_coupon"), 

    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path('complete_payment/<tran_id>/<payment_type>/', complete_payment, name='complete_payment'),


]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
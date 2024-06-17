from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from invoice.views import InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView


urlpatterns = [
    path('invoices/',InvoiceListView.as_view(), name="invoice_list"),
    path('invoice/<slug:slug>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('new-invoice/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoice/<slug:slug>/update/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoice/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
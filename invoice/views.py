from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from invoice.models import Invoice
from .tables import InvoiceTable




class InvoiceListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    model = Invoice
    table_class = InvoiceTable
    template_name = 'invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10
    SingleTableView.table_pagination = False


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoice_detail.html'

    def get_success_url(self):
        return reverse('invoice_detail',  kwargs={'slug': self.object.pk})



class InvoiceCreateView(LoginRequiredMixin,CreateView):
    model = Invoice
    template_name = 'invoice_create.html'
    fields = ['customer_name','contact_number','item','price_per_item','quantity', 'shipping',]

    def get_success_url(self):
        return reverse('invoice_list')

class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invoice
    template_name = 'invoice_update.html'
    fields = ['customer_name','contact_number','item','price_per_item','quantity','shipping',]

    def get_success_url(self):
        return reverse('invoice_list')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invoice
    template_name = 'invoice_delete.html'
    success_url = '/products'

    def get_success_url(self):
        return reverse('invoice_list')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
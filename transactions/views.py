from django.shortcuts import render

# Create your views here.
from transactions.models import Purchase, Sale
from django.contrib.auth.models import User
from .filters import PurchaseFilter, SaleFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from .tables import PurchaseTable, SaleTable
from django.core.exceptions import ValidationError
from accounts.models import Profile
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages

class PurchaseListView(ExportMixin, tables.SingleTableView):
    """View to list purchases and export them."""
    model = Purchase
    table_class = SaleTable
    template_name = 'purchase_list.html'
    context_object_name = 'purchases'
    paginate_by = 10
    SingleTableView.table_pagination = False

class PurchaseDetailView(FormMixin, DetailView):
    """"View to display details of a purchase."""
    model = Purchase
    template_name = 'sales_detail.html'

    def get_success_url(self):
        return reverse('sales_detail', kwargs={'slug': self.object.slug})

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    """View to create a new purchase."""
    model = Purchase
    template_name = 'purchase_create.html'
    fields = ['item', 'description', 'vendor', 'delivery_date', 'quantity', 'delivery_status']

    def form_valid(self, form):
        """Handles the form submission and updates the item's quantity."""
        item = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']

        total_value = item.selling_price * quantity

        form.instance.total_value = total_value
        form.instance.price = item.selling_price

        form.instance.balance = total_value

        form.instance.profile = self.request.user.profile

        item.quantity += quantity
        item.save()

        response = super().form_valid(form)
        messages.success(self.request, "Purchase Data has been successfully created.")
        return response

    def get_success_url(self):
        return reverse('purchase_list')

    def test_func(self):
        profile_list = Profile.objects.all()
        if self.request.user.profile in profile_list:
            return False
        else:
            return True

class PurchaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update a purchase."""
    model = Purchase
    template_name = 'purchase_update.html'
    fields = ['item', 'description', 'vendor', 'delivery_date', 'quantity', 'price', 'delivery_status']

    def test_func(self):
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False
    

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Purchase Data has been successfully updated.")
        return response

    def get_success_url(self):
            return reverse('purchase_list')


class PurchaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a purchase."""
    model = Purchase
    template_name = 'purchase_delete.html'

    def test_func(self):
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Purchase Data has been successfully deleted.")
        return response
    
    def get_success_url(self):
            return reverse('purchase_list')

class SaleListView(ExportMixin, tables.SingleTableView):
    """View to list sales and export them."""
    model = Sale
    table_class = SaleTable
    template_name = 'sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10
    SingleTableView.table_pagination = False

class SaleDetailView(DetailView):
    """View to display details of a sale."""
    model = Sale
    template_name = 'sales_detail.html'


class SaleCreateView(LoginRequiredMixin, CreateView):
    """View to create a new sale."""
    model = Sale
    template_name = 'sales_create.html'
    fields = ['item', 'first_name', 'payment_method', 'quantity', 'amount_received']

    def get_success_url(self):
        return reverse('sales_list')

    def form_valid(self, form):
        """Handles the form submission and validates product availability."""
        item = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']

        if item.quantity < quantity:
            raise ValidationError(f"Only {item.quantity} units of '{item.name}' are available.")

        price = item.selling_price

        total_price = price * quantity

        form.instance.price = price
        form.instance.total_value = total_price

        amount_received = form.cleaned_data['amount_received']
        balance = amount_received - total_price
        form.instance.balance = balance

        form.instance.profile = self.request.user.profile
        response = super().form_valid(form)
        messages.success(self.request, "Sales has been successfully created.")
        return response

    def test_func(self):
        profile_list = Profile.objects.all()
        if self.request.user.profile in profile_list:
            return False
        else:
            return True

class SaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update a sale."""
    model = Sale
    template_name = 'sales_update.html'
    fields = ['item', 'customer_name', 'payment_method', 'quantity', 'price', 'amount_received']

    def test_func(self):
        """Checks if the user has the required permissions to access this view."""
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('sales_list')

    def form_valid(self, form):
        """Handles form submission and sets the profile of the sale."""
        form.instance.profile = self.request.user.profile
        response = super().form_valid(form)
        messages.success(self.request, "Sales has been successfully updated.")
        return response
    
class SaleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a sale."""
    model = Sale
    template_name = 'sales_delete.html'


    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Sales has been successfully deleted.")
        return response
    
    def get_success_url(self):
        return reverse('sales_list')

    def test_func(self):
        """Checks if the user has the required permissions to access this view."""
        if self.request.user.is_superuser:
            return True
        else:
            return False
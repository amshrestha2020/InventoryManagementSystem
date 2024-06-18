from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from bills.models import Bill
from bills.tables import BillTable
from accounts.models import Profile
from django.contrib import messages



class BillListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """View for listing bills."""
    model = Bill
    table_class = BillTable
    template_name = 'bill_list.html'
    context_object_name = 'bills'
    paginate_by = 10
    SingleTableView.table_pagination = False


class BillCreateView(LoginRequiredMixin, CreateView):
    """View for creating a bill."""
    model = Bill
    template_name = 'bill_create.html'
    fields = ['institution_name', 'phone_number', 'email', 'address', 'description', 'payment_details', 'amount', 'status']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Bill has been successfully created.")
        return response
    
    def get_success_url(self):
        return reverse('bill_list')

class BillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a bill."""
    model = Bill
    template_name = 'bill_update.html'
    fields = ['institution_name', 'phone_number', 'email', 'address', 'description', 'payment_details', 'amount', 'status']

    def test_func(self):
        """Checks if the user has the required permissions to access this view."""
        return self.request.user.profile in Profile.objects.all()
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Bill has been successfully updated.")
        return response


    def get_success_url(self):
        return reverse('bill_list')


class BillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a bill."""
    model = Bill
    template_name = 'bill_delete.html'

    def test_func(self):
        """Checks if the user has the required permissions to access this view."""
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Bill has been successfully deleted.")
        return response
    
    def get_success_url(self):
        return reverse('bill_list')
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Vendor
from .forms import CustomerForm, VendorForm
from django.views.generic import ListView, CreateView
from functools import reduce
from django.db.models import Q, Count, Sum, Avg
import operator
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('user_login')
#     return render(request, 'templates/dashboard.html')


class HomeRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:  # Assuming admin users have 'is_staff' set to True
            return redirect('dashboard')
        else:
            return redirect('index')

class DashboardView(LoginRequiredMixin, View):
    template_name = 'templates/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# vendor_list

class VendorListView(ListView):
    model = Vendor
    template_name = 'vendor.html'
    context_object_name = 'vendors'


class VendorCreateView(CreateView):
    model = Vendor
    template_name = 'vendor_create.html'
    fields = ['name', 'photo', 'address', 'mobile', 'status']


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Vendor has been successfully created.")
        return response
    
    def get_success_url(self):
        return reverse('sales_list')

def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, "Vendor has been successfully updated.")
            return redirect('vendor')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor_edit.html', {'form':form})


def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        vendor.delete()
        messages.success(request, "Vendor has been successfully deleted.")
        return redirect('vendor')
    return render(request, 'vendor_delete.html', {'vendor': vendor})


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer has been successfully eduted.")
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_edit.html', {'form': form})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer has been successfully deleted.")
        return redirect('customer_list')
    return render(request, 'customer_confirm_delete.html', {'customer': customer})



class ItemSearchListView(CustomerListView):
    paginate_by = 10

    def get_queryset(self):
        result = super(ItemSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list']:
            messages.info(self.request, 'Match not found')
        return context

    def render_to_response(self, context, **response_kwargs):
        if not context['object_list']:
            return redirect('customer_list')  # replace 'customer_list' with the name of your customer list view
        else:
            return super().render_to_response(context, **response_kwargs)
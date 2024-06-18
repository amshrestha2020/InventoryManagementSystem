from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Vendor
from .forms import CustomerForm, VendorForm
from django.views.generic import ListView, CreateView
from functools import reduce
from django.db.models import Q, Count, Sum, Avg
import operator
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'templates/dashboard.html')


# vendor_list

class VendorListView(ListView):
    model = Vendor
    template_name = 'vendor.html'
    context_object_name = 'vendors'


class VendorCreateView(CreateView):
    model = Vendor
    template_name = 'vendor_create.html'
    fields = ['name', 'photo', 'address', 'mobile', 'status']


    def get_success_url(self):
        return reverse('sales_list')

def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save()
            return redirect('vendor')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor_edit.html', {'form':form})


def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        vendor.delete()
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
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_edit.html', {'form': form})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
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

                # If no items are found, add a message
        if not result.exists():
            messages.add_message(self.request, messages.INFO, 'Match Not found')

        return result
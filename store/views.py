from django.shortcuts import render

# Create your views here.
import operator
from functools import reduce
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from django.db.models import Q, Count, Sum, Avg
from django.views.generic.edit import FormMixin

from accounts.models import Profile, Vendor
from transactions.models import Sale
from store.models import Category, Item, Delivery
from store.forms import ProductForm
from store.tables import ItemTable
from django.contrib import messages

@login_required
def dashboard(request):
    profiles =  Profile.objects.all()
    Category.objects.annotate(nitem=Count('item'))
    items = Item.objects.all()
    total_items = Item.objects.all().aggregate(Sum('quantity')).get('quantity__sum', 0.00)
    items_count = items.count()
    profiles_count = profiles.count()

    #profile pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(profiles, 3)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    #items pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 4)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'profiles' : profiles,
        'profiles_count': profiles_count,
        'items_count': items_count,
        'total_items': total_items,
        'vendors' : Vendor.objects.all(),
        'delivery': Delivery.objects.all(),
        'sales': Sale.objects.all()
    }
    return render(request, 'dashboard.html', context)


class ProductListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    model = Item
    table_class = ItemTable
    template_name = 'products_list.html'
    context_object_name = 'items'
    paginate_by = 10
    ordering = ['id']
    SingleTableView.table_pagination = False

class ItemSearchListView(ProductListView):
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
            messages.add_message(self.request, messages.INFO, 'No items found')

        return result

class ProductDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Item
    template_name = 'products_detail.html'

    def get_success_url(self):
        return reverse('products_detail', kwargs={'slug': self.object.slug})

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'products_create.html'
    form_class = ProductForm
    
    def get_success_url(self):
        return reverse('products_list')

    def test_func(self):
        #item = Item.objects.get(id=pk)
        if self.request.POST.get("quantity") < 1:
            return False
        else:
            return True

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'products_update.html'
    fields = ['name','category','quantity','selling_price', 'expiring_date', 'vendor']
    
    
    def get_success_url(self):
        return reverse('products_list')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'products_delete.html'
    
    def get_success_url(self):
        return reverse('products_list')


    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

class DeliveryListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    model = Delivery
    pagination = 10
    template_name = 'deliveries.html'
    context_object_name = 'deliveries'

class DeliverySearchListView(DeliveryListView):
    paginate_by = 10

    def get_queryset(self):
        result = super(DeliverySearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(customer_name__icontains=q) for q in query_list))
            )
        return result

class DeliveryDetailView(LoginRequiredMixin, DetailView):
    """
    View class to display detailed information about a delivery.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    """
    model = Delivery
    template_name = 'delivery_detail.html'


class DeliveryCreateView(LoginRequiredMixin, CreateView):
    """
    View class to create a new delivery.

    Attributes:
    - model: The model associated with the view.
    - fields: The fields to be included in the form.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Delivery
    fields = ['item', 'customer_name', 'phone_number', 'location', 'date','is_delivered']
    template_name = 'delivery_create.html'

    def get_success_url(self):
        return reverse('deliveries')
    

class DeliveryUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update delivery information.

    Attributes:
    - model: The model associated with the view.
    - fields: The fields to be updated.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Delivery
    fields = ['item', 'customer_name', 'phone_number', 'location', 'date','is_delivered']
    template_name = 'delivery_update.html'

    def get_success_url(self):
        return reverse('deliveries')
    

class DeliveryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View class to delete a delivery.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful deletion.
    """
    model = Delivery
    template_name = 'products_delete.html'

    def get_success_url(self):
        return reverse('deliveries')
    

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
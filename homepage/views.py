from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
import random
import string

# Create your views here.
from django.views.generic import TemplateView, ListView, FormView, View, DetailView
from django.conf import settings
from .models import Setting, SettingLang, ContactMessage
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from .forms import SearchForm, CheckoutForm, CouponForm
from accounts.forms import ContactForm
from accounts.models import Language, FAQ, Profile
from store.models import Item, Category, Images, Comment, Variants, Cart, OrderItem, Address, Coupon, Payment, UserProfile
from django.utils import timezone

from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.db.models import Q


def Base(request):
    user = request.user
    product = Item.objects.all()
    
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cartitem = Item.objects.filter(cart=cart)
            quantity = 0
            for item in cartitem:
                quantity += item.quantity
            
            # Count total items in the order
            ordered = OrderItem.objects.filter(user=request.user, ordered=False).first()
            if ordered:
                total_items = ordered.item.count()
            else:
                total_items = 0


            return render(request, 'base.html', {'products': product, 'quantity': quantity, 'total_items': total_items})
        
        except Cart.DoesNotExist:
            # Handle the case where the cart does not exist
            return render(request, 'base.html', {'products': product, 'quantity': 0, total_items: 0})
    
    else:
        return render(request, 'base.html', {'products': product, 'total_items': 0})
    

class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 8
    ordering = '-id'

    def get_queryset(self):
        queryset = Item.objects.all()
        category = self.kwargs.get('category_name')
        search_by = self.request.GET.get('key')
        
        if category:
            queryset = queryset.filter(item_category__category=category)
        
        if search_by:
            queryset = queryset.filter(
                Q(item_category__category__icontains=search_by) |
                Q(item_name__icontains=search_by)
            )
        
        return queryset.order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add additional context variables
        host = self.request.get_host()
        categories = Category.objects.all()
        
        context['categories'] = categories
        context['host'] = host
        
        return context
    

    
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)



class AboutUsView(TemplateView):
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = request.LANGUAGE_CODE[0:2]
        setting = Setting.objects.get(pk=1)
        if defaultlang != currentlang:
            setting = SettingLang.objects.get(lang=currentlang)

        context = {'setting': setting}
        return self.render_to_response(context)
    



class ContactUsView(FormView):
    template_name = 'contactus.html'
    form_class = ContactForm
    success_url = '/contact'

    def form_valid(self, form):
        data = ContactMessage()
        data.name = form.cleaned_data['name']
        data.email = form.cleaned_data['email']
        data.subject = form.cleaned_data['subject']
        data.message = form.cleaned_data['message']
        data.ip = self.request.META.get('REMOTE_ADDR')
        data.save()
        messages.success(self.request, _("Your message has been sent. Thank you for your message."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = self.request.LANGUAGE_CODE[0:2]
        setting = Setting.objects.get(pk=1)
        if defaultlang != currentlang:
            setting = SettingLang.objects.get(lang=currentlang)
        context['setting'] = setting
        return context
    




class SearchView(FormView):
    form_class = SearchForm
    template_name = 'search_products.html'

    def form_valid(self, form):
        query = form.cleaned_data['query']
        catid = form.cleaned_data['catid']
        if catid == 0:
            products = Item.objects.filter(title__icontains=query)
        else:
            products = Item.objects.filter(title__icontains=query, category_id=catid)

        category = Category.objects.all()
        context = {
            'products': products,
            'query': query,
            'category': category
        }
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        return redirect('/')


class SearchAutoView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            q = request.GET.get('term', '')
            products = Item.objects.filter(title__icontains=q)

            results = []
            for rs in products:
                product_json = rs.title + " > " + rs.category.title
                results.append(product_json)
            return JsonResponse(results, safe=False)
        return JsonResponse({'error': 'Invalid request'}, status=400)
    



class ProductDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'
    context_object_name = 'product'
    
    def get_object(self):
        return get_object_or_404(Item, slug=self.kwargs['slug'])



class AjaxColorView(View):
    def post(self, request, *args, **kwargs):
        data = {}
        if request.POST.get('action') == 'post':
            size_id = request.POST.get('size')
            productid = request.POST.get('productid')
            colors = Variants.objects.filter(product_id=productid, size_id=size_id)
            context = {
                'size_id': size_id,
                'productid': productid,
                'colors': colors,
            }
            data = {'rendered_table': render_to_string('color_list.html', context=context)}
            return JsonResponse(data)
        return JsonResponse(data)

class FaqView(View):
    template_name = 'faq.html'

    def get(self, request):
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = request.LANGUAGE_CODE[0:2]

        if defaultlang == currentlang:
            faq = FAQ.objects.filter(status="True", lang=defaultlang).order_by("ordernumber")
        else:
            faq = FAQ.objects.filter(status="True", lang=currentlang).order_by("ordernumber")

        context = {'faq': faq}
        return render(request, self.template_name, context)




class ProductListView(View):
    template_name = 'product_list.html'

    def get(self, request):
        items = Item.objects.all()
        return render(request, self.template_name, {'items': items})


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            if order.items.count() == 0:
                return redirect("product_list")  # Redirect to item list if cart is empty
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            # Handle the case where the cart does not exist for the user
            return redirect("home")  # Redirect to home page if cart does not exist
        


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    ordered_item, is_created = OrderItem.objects.get_or_create(
        user=request.user,
        item=item,
        ordered=False
    )
    user_cart = Cart.objects.filter(user=request.user, ordered=False)
    if user_cart.exists():
        user_order = user_cart[0]
        filtered_user_cart_by_the_ordered_item = user_order.items.filter(item__slug=item.slug)
        if filtered_user_cart_by_the_ordered_item.exists():
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "The quantity was updated")
        else:
            user_order.items.add(ordered_item)
    # If user does not have any item in the cart create the new instance in the Order model
    else:
        new_order = Cart.objects.create(
            user=request.user,
            ordered_date=timezone.now(),
        )
        new_order.items.add(ordered_item)
        messages.info(request, "The item was added to the cart")
    return redirect("order_summary")




@login_required
def remove_from_the_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("product_detail", slug=slug)
    else:
        messages.info(request, "You have no order existed")
        return redirect("product_detail", slug=slug)
    return redirect("order_summary")


@login_required
def remove_single_from_the_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity == 1:
                order.items.remove(order_item)
                order_item.delete()
            else:
                order_item.quantity -= 1
                order_item.save()
            messages.info(request, "This quantity was updated")
        else:
            messages.info(request, "This item is not in your cart")
    else:
        messages.info(request, "You have no order existed")
        return redirect("order_summary")
    return redirect("order_summary")




def is_valid_form(list_of_values):
    valid = True
    for value in list_of_values:
        if value == "":
            return False
    return valid

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        try:
            order_items = Cart.objects.get(user=self.request.user, ordered=False)
            if order_items.items.count() == 0:
                messages.info(self.request, "No item in your cart")
                return redirect("main")
            context = {
                'form': form,
                "orders": order_items,
                'coupon_form': CouponForm(),
                'DISPLAY_COUPON_FORM': True
            }
            shipping_address_qs = Address.objects.filter(user=self.request.user,
                                                         address_type="S", is_default=True)
            if shipping_address_qs.exists():
                context.update({"default_shipping_address": shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(user=self.request.user,
                                                        address_type="B", is_default=True)
            if billing_address_qs.exists():
                context.update({"default_billing_address": billing_address_qs[0]})
            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "you dont have any order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # Shipping Address Handling
                set_default_shipping = form.cleaned_data.get('set_default_shipping')
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    shipping_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type="S",
                        is_default=True
                    )
                    if shipping_qs.exists():
                        shipping = shipping_qs[0]
                        order.shipping_address = shipping
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping")
                        return redirect("checkout")
                else:
                    shipping_address = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    if is_valid_form([shipping_address, shipping_address2, shipping_country]):
                        shipping = Address(
                            user=self.request.user,
                            street_address=shipping_address,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip_code=shipping_zip,
                            address_type="S"
                        )
                        if set_default_shipping:
                            shipping.is_default = True
                        shipping.save()
                        order.shipping_address = shipping
                        order.save()
                    else:
                        messages.info(self.request, "Please fill in the shipping form properly")
                        return redirect("checkout")
                # Billing Address Handling
                same_billing_address = form.cleaned_data.get('same_billing_address')
                use_default_billing = form.cleaned_data.get('use_default_billing')
                set_default_billing = form.cleaned_data.get('set_default_billing')
                if same_billing_address:
                    billing_address = shipping
                    billing_address.pk = None
                    billing_address.address_type = "B"
                    if not set_default_billing:
                        billing_address.is_default = False
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                elif use_default_billing:
                    billing_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type="B",
                        is_default=True
                    )
                    if billing_qs.exists():
                        billing = billing_qs[0]
                        order.billing_address = billing
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping")
                        return redirect("checkout")
                else:
                    billing_address = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')
                    if is_valid_form([billing_address, billing_address2, billing_country]):
                        billing = Address(
                            user=self.request.user,
                            street_address=billing_address,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip_code=billing_zip,
                            address_type="B"
                        )
                        if set_default_billing:
                            billing.is_default = True
                        billing.save()
                        order.billing_address = billing
                        order.save()
                    else:
                        messages.info(self.request, "Please fill the in billing form properly")
                        return redirect("checkout")
                # Payment Handling
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == "S":
                    return redirect("payment", payment_option="Stripe")
                elif payment_option == "P":
                    return redirect("payment", payment_option="Paypal")
                elif payment_option == "C":
                    return redirect("payment", payment_option="CASH")
                else:
                    # add redirect to selected payment method
                    return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "Error ")
            return redirect("checkout")


class AddCouponView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        order = Cart.objects.get(user=self.request.user, ordered=False)
        coupon_code = self.request.POST['coupon_code']
        available_coupons = Coupon.objects.filter(coupon=coupon_code)
        if available_coupons.exists():
            coupon = Coupon.objects.get(coupon=coupon_code)
            order.coupon = coupon
            order.save()
            messages.info(self.request, "coupon added")
            return redirect('checkout')
        else:
            messages.error(self.request, "There is no such coupon")
            return redirect('checkout')


def generate_reference_code():
    return "".join(random.choices(string.ascii_lowercase
                                + string.ascii_uppercase
                                + string.digits, k=20))





class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        payment_option = kwargs.get('payment_option')
        if payment_option == "SSL":
            return redirect('ssl_payment')
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            user_profile = self.request.user.userprofile
            if order.items.count() == 0:
                messages.info(self.request, "No item in your cart")
                return redirect("main")
            if order.billing_address:
                context = {
                    "orders": order,
                    'coupon_form': CouponForm(),
                    'DISPLAY_COUPON_FORM': False
                }
                
                return render(self.request, 'payment.html', context)
            else:
                messages.warning(self.request, "You have not added a billing address")
                return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You have no active order")
            return redirect("main")

    def post(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            userprofile = UserProfile.objects.get(user=self.request.user)
            amount = int(order.get_total())

            # Create a new payment object and mark it as paid by cash
            payment = Payment(
                user=self.request.user,
                amount=amount,
                payment_method="Cash",
                timestamp=timezone.now()
            )
            payment.save()

            # Assign the payment to the order and mark it as ordered
            order.payment = payment
            order.ordered = True
            order.save()

            # Clear the cart
            for item in order.items.all():
                item.ordered = True
                item.save()

            messages.success(self.request, "Your order was successful")
            return redirect('complete_payment', tran_id=payment.id, payment_type="Cash")

        except ObjectDoesNotExist:
            messages.warning(self.request, "You have no active order")
            return redirect("main")

        except Exception as e:
            messages.error(self.request, "A serious error occurred. We have been notified.")
            return redirect("payment", payment_option="Cash")
    



@login_required
def complete_payment(request, tran_id, payment_type):
    order = Cart.objects.get(user=request.user, ordered=False)
    amount = int(order.get_total())
    payment = Payment()
    payment.user = request.user
    payment.amount = amount
    payment.stripe_charge_id = tran_id
    payment.save()

    order.ordered = True
    order.payment = payment
    order.reference_code = generate_reference_code()
    order.save()
    users_order = OrderItem.objects.filter(user=request.user, ordered=False)
    for order in users_order:
        order.ordered = True
        order.save()
    return HttpResponseRedirect(reverse('checkout'))



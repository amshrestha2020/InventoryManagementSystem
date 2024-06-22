from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView, ListView, FormView, View
from django.conf import settings
from .models import Setting, SettingLang, ContactMessage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import translation
from django.views import View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from .forms import SearchForm
from accounts.forms import ContactForm
from accounts.models import Language, FAQ, Profile
from store.models import Item, Category, CategoryLanguage, ProductLanguage, Images, Comment, Variants, Cart

from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# class IndexView(TemplateView):
#     template_name = 'home.html'

#     def get(self, request, *args, **kwargs):
#         if not request.session.has_key('currency'):
#             request.session['currency'] = settings.DEFAULT_CURRENCY

#         try:
#             setting = Setting.objects.get(pk=1)
#         except Setting.DoesNotExist:
#             setting = None

#         products_latest = Item.objects.all().order_by('-id')[:4]

#         defaultlang = settings.LANGUAGE_CODE[0:2]
#         currentlang = request.LANGUAGE_CODE[0:2]

#         if defaultlang != currentlang:
#             setting = SettingLang.objects.get(lang=currentlang)
#             products_latest = Item.objects.raw(
#                 'SELECT p.id, p.price, l.title, l.description, l.slug '
#                 'FROM product_product as p '
#                 'LEFT JOIN product_productlang as l '
#                 'ON p.id = l.product_id '
#                 'WHERE l.lang=%s ORDER BY p.id DESC LIMIT 4', [currentlang])

#         products_slider = Item.objects.all().order_by('id')[:4]
#         products_picked = Item.objects.all().order_by('?')[:4]

#         page = "home"
#         context = {
#             'setting': setting,
#             'page': page,
#             'products_slider': products_slider,
#             'products_latest': products_latest,
#             'products_picked': products_picked,
#         }

#         if request.user.is_authenticated:
#             if request.user.is_superuser:
#                 return redirect('dashboard')
#             else:
#                 return self.render_to_response(context)
#         else:
#             return self.render_to_response(context)

def Base(request):
	user = request.user
	product = Item.objects.all()
	if user.is_authenticated:
		cart = Cart.objects.get(user=request.user)
		cartitem = Item.objects.filter(cart=cart)
		quantity = 0
		for item in cartitem:	
			quantity += item.quantity

		return render(request, 'base.html', {'products':product, 'quantity':quantity})
	else:
		return render(request, 'base.html', {'products':product})

def Home(request):
	user = request.user
	product = Item.objects.all()
	if user.is_authenticated:
		cart = Cart.objects.get(user=request.user)
		cartitem = Item.objects.filter(cart=cart)
		quantity = 0
		for item in cartitem:	
			quantity += item.quantity

		return render(request, 'home.html', {'products':product, 'quantity':quantity})
	else:
		return render(request, 'home.html', {'products':product})
    
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


class SelectLanguageView(View):
    def post(self, request, *args, **kwargs):
        cur_language = translation.get_language()
        lasturl = request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        return HttpResponseRedirect("/" + lang)



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
    



class CategoryProductsView(ListView):
    template_name = 'category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        id = self.kwargs['id']
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = self.request.LANGUAGE_CODE[0:2]
        if defaultlang == currentlang:
            return Item.objects.filter(category_id=id)
        else:
            return Item.objects.raw(
                'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                'FROM product_product as p '
                'LEFT JOIN product_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.category_id=%s and l.lang=%s', [id, currentlang]
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = self.request.LANGUAGE_CODE[0:2]
        catdata = get_object_or_404(Category, pk=id)
        if defaultlang != currentlang:
            try:
                catdata = get_object_or_404(CategoryLanguage, category_id=id, lang=currentlang)
            except CategoryLanguage.DoesNotExist:
                pass
        context['catdata'] = catdata
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
    



class ProductDetailView(View):
    template_name = 'product_detail.html'

    def get(self, request, id, slug):
        query = request.GET.get('q')
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = request.LANGUAGE_CODE[0:2]
        category = Category.objects.all()
        product = get_object_or_404(Item, pk=id)

        if defaultlang != currentlang:
            try:
                prolang = Item.objects.raw(
                    'SELECT p.id, p.price, p.amount, p.image, p.variant, l.title, l.keywords, l.description, l.slug, l.detail '
                    'FROM product_product as p '
                    'INNER JOIN product_productlang as l '
                    'ON p.id = l.product_id '
                    'WHERE p.id = %s and l.lang = %s', [id, currentlang])
                product = prolang[0]
            except:
                pass

        images = Images.objects.filter(product_id=id)
        comments = Comment.objects.filter(product_id=id, status='True')
        context = {'product': product, 'category': category, 'images': images, 'comments': comments}

        if product.variant != "None":
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id = %s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
            context.update({'sizes': sizes, 'colors': colors, 'variant': variant, 'query': query})

        return render(request, self.template_name, context)

    def post(self, request, id, slug):
        query = request.GET.get('q')
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = request.LANGUAGE_CODE[0:2]
        category = Category.objects.all()
        product = get_object_or_404(Item, pk=id)

        if defaultlang != currentlang:
            try:
                prolang = Item.objects.raw(
                    'SELECT p.id, p.price, p.amount, p.image, p.variant, l.title, l.keywords, l.description, l.slug, l.detail '
                    'FROM product_product as p '
                    'INNER JOIN product_productlang as l '
                    'ON p.id = l.product_id '
                    'WHERE p.id = %s and l.lang = %s', [id, currentlang])
                product = prolang[0]
            except:
                pass

        images = Images.objects.filter(product_id=id)
        comments = Comment.objects.filter(product_id=id, status='True')
        context = {'product': product, 'category': category, 'images': images, 'comments': comments}

        if product.variant != "None":
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id = %s GROUP BY size_id', [id])
            query += variant.title + ' Size: ' + str(variant.size) + ' Color: ' + str(variant.color)
            context.update({'sizes': sizes, 'colors': colors, 'variant': variant, 'query': query})

        return render(request, self.template_name, context)

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



class SelectCurrencyView(View):
    def post(self, request):
        lasturl = request.META.get('HTTP_REFERER')
        request.session['currency'] = request.POST['currency']
        return HttpResponseRedirect(lasturl)



@method_decorator(login_required(login_url='/login'), name='dispatch')
class SaveLangCurView(View):
    def post(self, request):
        lasturl = request.META.get('HTTP_REFERER')
        current_user = request.user
        language = get_object_or_404(Language, code=request.LANGUAGE_CODE[0:2])
        data = get_object_or_404(Profile, user_id=current_user.id)
        data.language_id = language.id
        data.currency_id = request.session['currency']
        data.save()
        return HttpResponseRedirect(lasturl)
    


class ProductListView(View):
    template_name = 'product_list.html'

    def get(self, request):
        items = Item.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(items, 9)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'product_list': items})

    def post(self, request):
        search_query = request.POST.get('search', '')
        items = Item.objects.filter(name__icontains=search_query)

        page = request.GET.get('page', 1)
        paginator = Paginator(items, 1)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'product_list': items})



class SortedProductListView(ListView):
    template_name = 'product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        keyword = self.kwargs['keyword']
        if keyword == 'allclothes':
            men_clothes = Category.objects.filter(title__icontains='menclothes')
            women_clothes = Category.objects.filter(title__icontains='womenclothes')
            return Item.objects.filter(category__in=men_clothes | women_clothes)
        else:
            # Ensure case-insensitive matching by using icontains on category title
            category = get_object_or_404(Category, title__iexact=keyword)
            return Item.objects.filter(category=category)


class UserSortedProductListView(ListView):
    template_name = 'product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        keyword = self.kwargs['keyword']
        if keyword == 'allclothes':
            return Item.objects.filter(category__icontains='menclothes') | Item.objects.filter(category__icontains='menclothes womenclothes')
        else:
            return Item.objects.filter(category__iexact = str(keyword))



class UserProductListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'user_products.html'
    context_object_name = 'productlist'
    login_url = 'login'  # URL to redirect to when the user is not logged in

    def get_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from accounts.tables import ProfileTable

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .tokens import account_activation_token

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )

# Create your views here.

from django.conf import settings  # Import settings here

from django.contrib.auth.views import RedirectURLMixin, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class LoginView(RedirectURLMixin, FormView):
    authentication_form = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return super().form_valid(form)



class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('user_login'))  # Redirect to a page of your choice


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'activation_success.html')
    else:
        return render(request, 'activation_invalid.html')
    

# def register(request):
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return redirect('user_login')
#     else:
#         form = CreateUserForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'register.html', context)


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            # Send registration confirmation mail
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            # Debugging prints
            print(f"Email Subject: {mail_subject}")
            print(f"Email Message: {message}")
            print(f"To Email: {to_email}")
            print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
            print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
            print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")


            send_mail(mail_subject, message, 'your-email@example.com', [to_email])
            return render(request, 'verification_sent.html')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    context = {

    }
    return render(request, 'profile.html', context)


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile_update.html', context)

class ProfileListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    model = Profile
    template_name = 'stafflist.html'
    context_object_name = 'profiles'
    pagination = 10
    table_class = ProfileTable
    SingleTableView.table_pagination = False

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'staffcreate'
    fields = ['user','role', 'status']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('profile_list')

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'staffupdate.html'
    fields = ['user','role', 'status']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse('profile_list')


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'staffdelete.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
    def get_success_url(self):
        return reverse('profile_list')
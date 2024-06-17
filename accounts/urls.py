from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as user_views
from django.conf.urls.static import static
from .views import (
    ProfileListView,
    ProfileCreateView,
    ProfileUpdateView,
    ProfileDeleteView,
    CustomLogoutView,
)
urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('register/', user_views.register, name='user_register'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='user_login'),
    path('profile/', user_views.profile, name='user_profile'),
    path('profile/update/', user_views.profile_update,name='user_profile_update'),
    path('logout/', CustomLogoutView.as_view(template_name='logout.html'), name='user_logout'),
    path('profiles/',ProfileListView.as_view(), name="profile_list"),
    path('new-profile/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:pk>/update/', ProfileDeleteView.as_view(), name='profile_delete')
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
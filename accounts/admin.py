from django.contrib import admin

# Register your models here.
from accounts.models import Profile


@admin.register(Profile)
class StatisticDiff(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'email', 'role', 'status')

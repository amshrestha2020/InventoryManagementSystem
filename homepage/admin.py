from django.contrib import admin

# Register your models here.
from .models import Setting, ContactMessage, FAQ, Language, SettingLang


class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','language','status']
    list_filter = ['status','language']

class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code','status']
    list_filter = ['status']


class SettingLangAdmin(admin.ModelAdmin):
    list_display = ['title', 'keywords','description','language']
    list_filter = ['language']

admin.site.register(Setting,SettingtAdmin)
admin.site.register(SettingLang,SettingLangAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(Language,LanguagesAdmin)
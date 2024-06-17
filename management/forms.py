# forms.py
from django import forms
from .models import Customer, Vendor

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'mobile', 'address', 'city', 'pin_code', 'country']



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'photo', 'address', 'mobile', 'status']

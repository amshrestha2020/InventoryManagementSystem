from django.db import models
from django_extensions.db.fields import AutoSlugField
from store.models import Item
from transactions.models import Sale, Purchase

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="vendor")
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    status = models.BooleanField()
    slug = AutoSlugField(unique=True , populate_from='name')


    class Meta:
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.name

class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.title


class Customer(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=100, default='Unknown') 
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='Unknown')

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, 
        default=0, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, 
        default=0, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    
    purchase_quantity = models.FloatField(default=0, null=True)
    sale_quantity = models.FloatField(default=0, null=True)
    #total_balance_quantity is expressed as, total_balance_quantity = purchase_quantity - sale_quantity
    total_balance_quantity = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Inventory'
    
    def product_unit(self):
        return self.product.unit.title

    def purchase_date(self):
        if self.purchase:
            return self.purchase.purchase_date

    def sale_date(self):
        if self.sale:
            return self.sale.sale_date
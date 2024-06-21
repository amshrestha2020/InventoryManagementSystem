from django.db import models

# Create your models here.

from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from management.models import Vendor
from django.forms import ModelForm
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models import Avg, Count
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from accounts.models import Language

# class Category(models.Model):
#     """
#     Represents a category for items.
#     """
#     name = models.CharField(max_length=50)
#     slug = AutoSlugField(unique=True , populate_from='name')

#     def __str__(self):
#         """
#         String representation of the category.
#         """
#         return f"Category: {self.name}"

#     class Meta:
#         verbose_name_plural = 'Categories'




class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Item(models.Model):
    """
    Represents an item in the inventory.
    """
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )

    slug = AutoSlugField(unique=True , populate_from='name')
    name = models.CharField(max_length=50, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.00)
    selling_price = models.FloatField(default=0)
    expiring_date = models.DateTimeField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/',null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount = models.IntegerField(default=0)
    minamount = models.IntegerField(default=3)
    variant = models.CharField(max_length=10,choices=VARIANTS, default='None')
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


    def __str__(self):
        return f"{self.name} - Category: {self.category}, Quantity: {self.quantity}"

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'slug': self.slug})

    def averagereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avg=Avg('rate'))
        average = 0
        if reviews["avg"] is not None:
            average = float(reviews["avg"])
        return average

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Items"

class Delivery(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(blank=True, null=True, max_length=30)
    phone_number = PhoneNumberField(null=True, blank=True)
    location = models.CharField(blank=True, null=True, max_length=20)
    date = models.DateTimeField(null=False, blank=False)
    is_delivered = models.BooleanField(default=False, verbose_name='is-delivered')

    def __str__(self):
        return (
            f"Delivery of {self.item} to {self.customer_name} "
            f"at {self.location} on {self.date}"
        )
    


class Images(models.Model):
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)

    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


llist= Language.objects.all()
list1=[]
for rs in llist:
    list1.append((rs.code,rs.name))
langlist= (list1)


class ProductLanguage(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE) #many to one relation with Category
    language =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    detail=RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('products_detail', kwargs={'slug': self.slug})

class CategoryLanguage(models.Model):
    category = models.ForeignKey(Category, related_name='categorylanguages', on_delete=models.CASCADE) #many to one relation with Category
    language =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    description = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
from django.db import models

# Create your models here.

from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from accounts.models import Language
from django.conf import settings
from django_countries import countries
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_save



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    on_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
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
        return reverse("item_list_by_category", kwargs={
            "category_name": self.title
        })



LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping')
)



COLOR_CHOICES = [
        ('BR', 'Brown'),
        ('BK', 'Black'),
        ('BL', 'Blue'),
        # Add more color choices as needed
    ]

SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    # Add more size choices as needed
]

TYPE_CHOICES = [
    ('R', 'Regular'),
    ('S', 'Slim'),
    # Add more type choices as needed
]

MATERIAL_CHOICES = [
    ('C', 'Cotton'),
    ('J', 'Jeans'),
    # Add more material choices as needed
]

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    item_image = models.ImageField(upload_to='items_images/')
    labels = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    description = models.TextField()

    color = models.CharField(choices=COLOR_CHOICES, max_length=2, blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=1, blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    materials = models.CharField(choices=MATERIAL_CHOICES, max_length=1, blank=True, null=True)


    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('homepage:products', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse('add_to_cart', kwargs={
            'slug': self.slug
        })

    def remove_from_the_cart(self):
        return reverse('remove_from_the_cart', kwargs={
            'slug':self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_price(self):
        return self.item.price * self.quantity


    def get_discounted_price(self):
        return self.item.discount_price if self.item.discount_price else self.item.price

    
    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price if self.item.discount_price else self.get_total_price()
    
    def get_tax(self):
        return 0.1 * self.get_total_price()  # assuming 10% tax
    
    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_price()
    #     else:
    #         return self.get_total_price()


    def get_final_price(self):
        total_price = self.get_total_price()
        total_discount = self.get_total_discount_price()
        tax = self.get_tax()
        return total_price + tax - total_discount



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    custom_choices = [('', 'Select Country')] + list(countries)
    country = models.CharField(max_length=2, choices=custom_choices)    
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    


class Coupon(models.Model):
    coupon = models.CharField(max_length=30)
    amount = models.IntegerField()

    def __str__(self):
        return self.coupon
    


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50, null=True, blank=True)
    ssl_charge_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    billing_address = models.ForeignKey('Address', related_name='billing_address',
                                        on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    reference_code = models.CharField(max_length=20)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Ensure a default value is provided

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        if self.coupon is not None:
            total -= self.coupon.amount
        return total
    

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_discount_price(self):
        return sum(item.get_total_discount_price() for item in self.items.all())

    def get_tax(self):
        return 0.1 * self.get_total_price()  # assuming 10% tax

    def get_final_price(self):
        total_price = Decimal(self.get_total_price())
        shipping_charge = Decimal(self.shipping_charge)
        tax = Decimal(self.get_tax())
        total_discount_price = Decimal(self.get_total_discount_price())
        
        return total_price + shipping_charge + tax - total_discount_price

class Refund(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=20)
    reason = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return str(self.pk)




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



@receiver(post_save, sender=User)
def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Signal to create user profile every time a new user is created
post_save.connect(user_profile_receiver, sender=settings.AUTH_USER_MODEL)
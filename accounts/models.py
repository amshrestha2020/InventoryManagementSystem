from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.fields import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, Textarea
from currencies.models import Currency

from django.utils.safestring import mark_safe


STATUS_CHOICES = [
    ('INA', 'Inactive'),
    ('A', 'Active'),
    ('OL', 'On_leave')
]

ROLE_CHOICES = [
    ('OP', 'Operative'),
    ('EX', 'Executive'),
    ('AD', 'Admin')
]


class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    status=models.BooleanField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, verbose_name=('Account ID'), populate_from='email')
    profile_picture = ProcessedImageField(default='profile_pics/default.jpg', upload_to='profile_pics', format='JPEG',
                                processors = [ResizeToFill(150,150)],
                                options={ 'quality': 100})
    telephone = PhoneNumberField(null=True,blank=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, blank=False, null=False, default='INA')
    role = models.CharField(choices=ROLE_CHOICES, max_length=12, blank=True, null=True)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True,blank=True)

    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        ordering = ["slug"]





class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=100)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    smtpserver = models.CharField(blank=True,max_length=50)
    smtpemail = models.CharField(blank=True,max_length=50)
    smtppassword = models.CharField(blank=True,max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class SettingLanguage(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    
    def __str__(self):
        return self.title
    

class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name= models.CharField(blank=True,max_length=20)
    email= models.CharField(blank=True,max_length=50)
    subject= models.CharField(blank=True,max_length=50)
    message= models.TextField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    language =  models.CharField(max_length=6, blank=True, null=True)
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
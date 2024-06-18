# Generated by Django 5.0.6 on 2024-06-11 23:25

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='date', unique=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date (eg: 2022/11/22)')),
                ('institution_name', models.CharField(max_length=30)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_details', models.CharField(max_length=255)),
                ('amount', models.FloatField(verbose_name='Total Amount Owing (Ksh)')),
                ('status', models.BooleanField(default=False, verbose_name='Paid')),
            ],
        ),
    ]

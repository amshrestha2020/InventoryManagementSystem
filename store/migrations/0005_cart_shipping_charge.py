# Generated by Django 5.0.6 on 2024-07-10 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='shipping_charge',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
    ]
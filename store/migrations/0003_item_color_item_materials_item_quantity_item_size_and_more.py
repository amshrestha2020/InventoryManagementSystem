# Generated by Django 5.0.6 on 2024-06-26 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_item_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(blank=True, choices=[('BR', 'Brown'), ('BK', 'Black'), ('BL', 'Blue')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='materials',
            field=models.CharField(blank=True, choices=[('C', 'Cotton'), ('J', 'Jeans')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(blank=True, choices=[('R', 'Regular'), ('S', 'Slim')], max_length=1, null=True),
        ),
    ]
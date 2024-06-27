# Generated by Django 5.0.6 on 2024-06-25 17:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.RenameField(
            model_name='item',
            old_name='category',
            new_name='item_category',
        ),
        migrations.RemoveField(
            model_name='item',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='item',
            name='create_at',
        ),
        migrations.RemoveField(
            model_name='item',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='item',
            name='expiring_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.RemoveField(
            model_name='item',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='item',
            name='minamount',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='selling_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='status',
        ),
        migrations.RemoveField(
            model_name='item',
            name='title',
        ),
        migrations.RemoveField(
            model_name='item',
            name='update_at',
        ),
        migrations.RemoveField(
            model_name='item',
            name='variant',
        ),
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='item_image',
            field=models.ImageField(default=1, upload_to='items_images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='item_name',
            field=models.CharField(default=8, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='labels',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='likes',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
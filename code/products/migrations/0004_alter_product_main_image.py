# Generated by Django 4.1.5 on 2023-03-15 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d/', verbose_name='Main Image'),
        ),
    ]
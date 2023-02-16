# Generated by Django 4.1.5 on 2023-02-16 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller_products', '0002_sellerproduct_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('New', 'New'), ('ProcessInProgress', 'Processinprogress'), ('Cancel', 'Cancel'), ('Paid', 'Paid')], default='New', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(limit_choices_to={'user_type': 'Customer'}, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('amount_currency', models.CharField(choices=[('KZT', 'Kzt'), ('USD', 'Usd')], max_length=3)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='orders.order')),
                ('seller_product', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='seller_products.sellerproduct')),
            ],
        ),
    ]

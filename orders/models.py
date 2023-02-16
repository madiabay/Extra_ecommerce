from django.contrib.auth import get_user_model
from django.db import models

from users import choices as user_choices
from seller_products import choices as seller_product_choices
from . import choices


class Order(models.Model):
    customer = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        related_name='orders',
        limit_choices_to={'user_type': user_choices.UserTypeChoices.Customer}
    )
    status = models.CharField(
        max_length=20,
        choices=choices.OrderStatusChoices.choices,
        default=choices.OrderStatusChoices.New
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    seller_product = models.ForeignKey(
        to='seller_products.SellerProduct',
        on_delete=models.PROTECT,
        related_name='order_items',
        limit_choices_to={'is_active': True}
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)
    amount_currency = models.CharField(
        max_length=3,
        choices=seller_product_choices.CurrencyChoices.choices
    )

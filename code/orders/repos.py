from typing import OrderedDict, Protocol
from django.db.models import QuerySet, Sum
from django.db import transaction

from . import models
from payments import models as payment_models
from seller_products import choices as seller_product_choices


class OrderReposInterface(Protocol):

    @staticmethod
    def create_order(data: OrderedDict) -> models.Order: ...

    @staticmethod
    def get_orders() -> QuerySet[models.Order]: ...


class OrderReposV1:

    @staticmethod
    def create_order(data: OrderedDict) -> models.Order:
        with transaction.atomic():
            order_items = data.pop('order_items')
            order = models.Order.objects.create(**data)
            models.OrderItem.objects.bulk_create([
                models.OrderItem(
                    order=order,
                    seller_product=i['seller_product'],
                    amount=i['seller_product'].amount,
                    amount_currency=i['seller_product'].amount_currency,
                ) for i in order_items
            ])

            total = order.order_items.aggregate(total=Sum('amount'))['total']
            payment_models.Bill.objects.create(
                order=order,
                total=total,
                amount=total,
                amount_currency=seller_product_choices.CurrencyChoices.KZT,
                number=payment_models.Bill.generate_number()
            )

        return order
    
    @staticmethod
    def get_orders() -> QuerySet[models.Order]:
        return models.Order.objects.all()
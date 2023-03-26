from typing import OrderedDict, Protocol
from django.db.models import QuerySet
from django.utils import timezone

from . import models, repos
from payments import tasks as payment_tasks


class OrderServicesInterface(Protocol):
    order_repos: repos.OrderReposInterface

    def create_order(self, data: OrderedDict) -> models.Order: ...

    def get_orders(self) -> QuerySet[models.Order]: ...


class OrderServicesV1:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    def create_order(self, data: OrderedDict) -> models.Order:
        order, bill = self.order_repos.create_order(data=data)
        payment_tasks.check_bill_expires_at.apply_async((bill.id,), eta=bill.expires_at)

        return order

    def get_orders(self) -> QuerySet[models.Order]:
        return self.order_repos.get_orders()

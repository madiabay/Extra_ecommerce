import pytest

from django.contrib.auth import get_user_model
from django.db.models import Sum

from seller_products.models import SellerProduct
from seller_products import choices
from products import models
from orders import repos

from django.test import Client
from rest_framework import status
import helpers


@pytest.mark.django_db
class CreateOrderReposTest:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    def test_create_order(self):
        customer = get_user_model().objects.get(phone_number='+77082698955')
        seller_product = SellerProduct.objects.get()
        order_items = [
            {'seller_product': seller_product}
        ]

        data = {
            'customer': customer,
            'order_items': order_items
        }

        order = self.order_repos.create_order(data=data)

        assert order.order_items.count() == len(order_items)

        total = order.order_items.aggregate(total=Sum('amount'))['total']
        
        assert total == sum(i['seller_product'].amount for i in order_items)

        assert all(
            i.amount_currency == choices.CurrencyChoices.KZT for i in order.order_items.all()
        )


@pytest.mark.django_db
class OrderViewTest(object):
    
    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')
    
    def test_create_order(self, api_client):
        customer = get_user_model().objects.get(phone_number='+77082698955')
        data = helpers.load_json_data(path='orders/create_order/1')

        response = api_client.post(
            '/api/v1/orders/',
            format='json',
            data=data,
            HTTP_AUTHORIZATION=helpers.access_token(user=customer)
        )

        assert response.status_code == status.HTTP_201_CREATED

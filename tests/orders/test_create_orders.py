import pytest

from django.contrib.auth import get_user_model
from django.db.models import Sum

from seller_products.models import SellerProduct
from payments import models as payment_models, choices as payment_choices
from orders import repos

from rest_framework import status
import helpers

from django.utils import timezone
import datetime


@pytest.mark.django_db
class CreateOrderReposTest:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures(
            'users.json', 'products.json', 'seller_products.json', 'orders.json', 'bills.json'
        )

    @pytest.mark.parametrize('user_id, seller_product_ides', (
        ('916824df-f4a7-4b82-a3de-760bff141323', (1,)),
        ('916824df-f4a7-4b82-a3de-760bff141323', (1, 2))
    ))
    @pytest.mark.freeze_time('2020-01-01')
    def test_create_order(self, user_id, seller_product_ides):
        user = get_user_model().objects.get(pk=user_id)
        seller_products = SellerProduct.objects.filter(id__in=seller_product_ides)
        order_items = [{'seller_product': seller_product} for seller_product in seller_products]

        data = {
            'customer': user,
            'order_items': order_items
        }

        order, bill = self.order_repos.create_order(data=data)

        assert order.order_items.count() == len(order_items)

        total = order.order_items.aggregate(total=Sum('amount'))['total']
        
        assert total == sum(i['seller_product'].amount for i in order_items)

        assert bill.amount == bill.total == total
        assert bill.status == payment_choices.BillStatusChoices.New

        assert bill.expires_at == timezone.now() + datetime.timedelta(minutes=30)


@pytest.mark.django_db
class OrderViewTest(object):
    
    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')
    
    @pytest.mark.parametrize('case, user_id, status_code', (
            ('1', '916824df-f4a7-4b82-a3de-760bff141323', status.HTTP_201_CREATED),
            ('2', '916824df-f4a7-4b82-a3de-760bff141323', status.HTTP_201_CREATED),
            ('3', '916824df-f4a7-4b82-a3de-760bff141323', status.HTTP_400_BAD_REQUEST),
            ('4', '916824df-f4a7-4b82-a3de-760bff141323', status.HTTP_400_BAD_REQUEST),
            ('5', '916824df-f4a7-4b82-a3de-760bff141323', status.HTTP_400_BAD_REQUEST),
            ('1', 'c1313f51-5118-4d47-9721-77a18c728d11', status.HTTP_403_FORBIDDEN),
    ))
    def test_create_order(self, case, user_id, status_code, api_client):
        user = get_user_model().objects.get(pk=user_id)
        data = helpers.load_json_data(path=f'orders/create_order/{case}')

        response = api_client.post(
            '/api/v1/orders/',
            format='json',
            data=data,
            HTTP_AUTHORIZATION=helpers.access_token(user=user)
        )

        assert response.status_code == status_code

# from decimal import Decimal
# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.db.models import Sum

# from products.models import Product
# from seller_products.models import SellerProduct
# from users.choices import UserTypeChoices
# from seller_products.choices import CurrencyChoices

# from orders.repos import OrderReposInterface, OrderReposV1


# class OrderTestCase(TestCase):
#     order_repos: OrderReposInterface = OrderReposV1()

#     def setUp(self) -> None:
#         customer = get_user_model().objects.create(
#             phone_number='+77082698955',
#             email='customer@mail.ru',
#         )
#         customer.user_type = UserTypeChoices.Customer
#         customer.save()

#         seller = get_user_model().objects.create(
#             phone_number='+77082698956',
#             email='seller@mail.ru',
#         )
#         seller.user_type = UserTypeChoices.Seller
#         seller.save()

#         product = Product.objects.create(
#             title='product 1',
#             body='some info',
#             data={
#                 'data': 'data'
#             },
#             main_image=None
#         )

#         seller_product = SellerProduct.objects.create(
#             product=product,
#             seller=seller,
#             amount = Decimal(10000),
#             amount_currency = CurrencyChoices.KZT
#         )
    
#     def test_create_order(self):
#         customer = get_user_model().objects.get(phone_number='+77082698955')
#         seller_product = SellerProduct.objects.get()
#         order_items = [
#             {'seller_product': seller_product}
#         ]

#         data = {
#             'customer': customer,
#             'order_items': order_items
#         }

#         order = self.order_repos.create_order(data=data)

#         self.assertEqual(order.order_items.count(), len(order_items))

#         total = order.order_items.aggregate(total=Sum('amount'))['total']
#         self.assertEqual(
#             total,
#             sum(i['seller_product'].amount for i in order_items)
#         )
        
#         self.assertTrue(
#             all(i.amount_currency == CurrencyChoices.KZT for i in order.order_items.all())
#         )
    
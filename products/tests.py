from django.test import TestCase

from products.models import Product


class ProductTestCase(TestCase):

    def setUp(self) -> None:
        Product.objects.create(
            title='product 1',
            body='some info',
            data={
                'data': 'data'
            },
            main_image=None
        )
    
    def test_product_is_top(self):
        product = Product.objects.get(title='product 1')
        self.assertEqual(product.is_top, False)
    
    def test_product_is_active(self):
        product = Product.objects.get(title='product 1')
        self.assertEqual(product.is_active, True)

from typing import Protocol
from django.db.models import Q, Min, QuerySet

from . import models


class ProductReposInterface(Protocol):
    
    @staticmethod
    def get_products() -> QuerySet[models.Product] | None: ...

class ProductImageReposInterface(Protocol):
    
    @staticmethod
    def get_product_images() -> QuerySet[models.ProductImage] | None: ...


class ProductReposV1:
    
    @staticmethod
    def get_products() -> QuerySet[models.Product] | None:
        return models.Product.objects.annotate(
            min_amount=Min('seller_products__amount', filter=Q(seller_products__is_active=True))
        )

class ProductImageReposV1:
    
    @staticmethod
    def get_product_images() -> QuerySet[models.ProductImage] | None:
        return models.ProductImage.objects.all()

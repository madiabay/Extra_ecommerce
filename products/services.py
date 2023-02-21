from typing import Protocol
from django.db.models import QuerySet

from . import models, repos


class ProductServicesInterface(Protocol):
    product_repos: repos.ProductReposInterface
    
    def get_products(self) -> QuerySet[models.Product] | None: ...

class ProductImageServicesInterface(Protocol):
    product_image_repos: repos.ProductImageReposInterface
    
    def get_product_images(self) -> QuerySet[models.ProductImage] | None: ...


class ProductServicesV1:
    product_repos: repos.ProductReposInterface = repos.ProductReposV1()
    
    def get_products(self) -> QuerySet[models.Product] | None:
        return self.product_repos.get_products()

class ProductImageServicesV1:
    product_image_repos: repos.ProductImageReposInterface = repos.ProductImageReposV1()
    
    def get_product_images(self) -> QuerySet[models.ProductImage] | None:
        return self.product_image_repos.get_product_images()

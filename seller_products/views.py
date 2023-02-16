from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class SellerProductViewSet(ModelViewSet):

    queryset = models.SellerProduct.objects.select_related('product', 'seller')
    serializer_class = serializers.SellerProductSerializer
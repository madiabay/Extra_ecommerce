from rest_framework.viewsets import ModelViewSet

from utils import mixins
from . import models, serializers


class ProductImageViewSet(ModelViewSet):

    queryset = models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer
    }
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
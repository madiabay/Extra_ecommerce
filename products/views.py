from django.db.models import Min, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from utils import mixins
from . import models, serializers, permissions


class ProductImageViewSet(ModelViewSet):

    queryset = models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = IsAuthenticated,


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer
    }
    queryset = models.Product.objects.annotate(
        min_amount=Min('seller_products__amount', filter=Q(seller_products__is_active=True))
    )
    serializer_class = serializers.ProductSerializer
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        
        return (permissions.IsMe(),)
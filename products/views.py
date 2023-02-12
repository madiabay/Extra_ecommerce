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
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (IsAuthenticated(),)
        
        return (permissions.IsMe(),)
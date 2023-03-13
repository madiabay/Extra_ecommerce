from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from utils import mixins
from . import services, serializers, permissions


class ProductImageViewSet(ModelViewSet):
    product_image_services: services.ProductImageServicesInterface = services.ProductImageServicesV1()

    queryset = product_image_services.get_product_images()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = permissions.IsAdminOrReadOnly,


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    product_services: services.ProductServicesInterface = services.ProductServicesV1()

    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer
    }

    queryset = product_services.get_products()
    serializer_class = serializers.ProductSerializer
    
    permission_classes = permissions.IsAdminOrReadOnly,
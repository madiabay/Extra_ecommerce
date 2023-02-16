from rest_framework import serializers

from . import models


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    min_amount = serializers.DecimalField(read_only=True, max_digits=14, decimal_places=2)

    class Meta:
        model = models.Product
        fields = '__all__'


class RetrieveProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    product_images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = models.Product
        fields = '__all__'
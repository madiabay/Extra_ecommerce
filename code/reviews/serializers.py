from rest_framework import serializers

from . import models


class ReviewSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = '__all__'

    def get_reviews(self, obj):
        return ReviewSerializer(obj.reviews.all(), many=True).data

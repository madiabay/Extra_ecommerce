from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Review(models.Model):
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='review',
    )
    parent_review = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )
    body = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(5)),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = '-created_at',

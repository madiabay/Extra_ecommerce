from django.db import models

class CurrencyChoices(models.TextChoices):
    KZT = 'KZT'
    USD = 'USD'
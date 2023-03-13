from django.db.models import signals
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver

from users import choices as user_choices
from . import models


User = get_user_model()


@receiver(signals.post_save, sender=models.Product)
def send_email_to_sellers(sender, instance: models.Product, created: bool, **kwargs):
    if created:
        sellers = User.objects.filter(user_type=user_choices.UserTypeChoices.Seller)
        seller_emails = [s.email for s in sellers]

        send_mail(
            f'NEW PRODUCT -> {instance.title}',
            f'Here is the message:\n\n  {instance.body}',
            settings.EMAIL_HOST_USER,
            seller_emails,
        )
import uuid

from src.celery import app
from django.utils import timezone

from payments import models, choices


@app.task()
def check_bill_expires_at(bill_id: uuid.UUID):
    models.Bill.objects.filter(
        id=bill_id,
        status=choices.BillStatusChoices.New,
        expires_at__lt=timezone.now(),
    ).update(
        status=choices.BillStatusChoices.Expired,
    )
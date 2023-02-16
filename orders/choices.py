from django.db.models import TextChoices


class OrderStatusChoices(TextChoices):
    New = 'New'
    ProcessInProgress = 'ProcessInProgress'
    Cancel = 'Cancel'
    Paid = 'Paid'
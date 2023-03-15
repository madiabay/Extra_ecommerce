from django.db import models


class BillStatusChoices(models.TextChoices):
    New = 'New'
    Pending = 'Pending' # в ожидании
    Paid = 'Paid'
    Expired = 'Expired' # истекший
    Refund = 'Refund' # возвращать деньги
    RefundPartially = 'RefundPartially' # частичный


class TransactionType(models.TextChoices):
    Ok = 'Ok'
    Refund = 'Refund' # возвращать деньги
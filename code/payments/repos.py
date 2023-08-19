import logging
import uuid

from typing import Protocol

from django.db import transaction

from . import models, choices


logger = logging.getLogger(__name__)

class BillReposInterface(Protocol):
    
    @staticmethod
    def pay_bill(bill_id: uuid.UUID) -> None: ...


class BillReposV1:
    
    @staticmethod
    def pay_bill(bill_id: uuid.UUID) -> None:
        try:
            with transaction.atomic():
                bill = models.Bill.objects.get(pk=bill_id)
                bill.status = choices.BillStatusChoices.Paid

                models.Transaction.objects.create(
                    bill=bill,
                    amount=bill.amount,
                    amount_currency=bill.amount_currency,
                    transaction_type=choices.TransactionType.Ok
                )
        except models.Bill.DoesNotExist:
            logger.error(f'bill with id {bill_id} not found')
        finally:
            logger.info(f'bill with id {bill_id} is successfully paid!')

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from . import services


class BillViewSet(ViewSet):
    bill_services: services.BillServicesInterface = services.BillServicesV1()

    def pay_bill(self, request, *args, **kwargs):
        bill_id = kwargs['bill_id']
        self.bill_services.pay_bill(bill_id=bill_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
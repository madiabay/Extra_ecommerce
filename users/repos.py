from typing import OrderedDict, Protocol
from . import models


class UserReposInterface(Protocol):

    def create_user(self, data: OrderedDict) -> models.CustomUser: ...


class UserReposV1:
    model = models.CustomUser

    def create_user(self, data: OrderedDict) -> models.CustomUser:
        return self.model.objects.create_user(**data)
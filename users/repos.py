from rest_framework.generics import get_object_or_404
from typing import OrderedDict, Protocol
from . import models


class UserReposInterface(Protocol):

    def create_user(self, data: OrderedDict) -> models.CustomUser: ...

    def get_user(self, data: OrderedDict) -> models.CustomUser: ...


class UserReposV1:
    model = models.CustomUser

    def create_user(self, data: OrderedDict) -> models.CustomUser:
        return self.model.objects.create_user(**data)

    def get_user(self, data: OrderedDict) -> models.CustomUser:
        user = get_object_or_404(self.model, email=data['email'])
        
        if not user.check_password(data['password']):
            raise self.model.DoesNotExist
        
        return user
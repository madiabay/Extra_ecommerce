from rest_framework.permissions import DjangoObjectPermissions

from . import models


class IsMe(DjangoObjectPermissions):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user
            and request.user.is_authenticated
            and request.user.email == 'madi@gmail.com'
        )
    
    def has_object_permission(self, request, view, obj: models.Product):
        return obj.user == request.user
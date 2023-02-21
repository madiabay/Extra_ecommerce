from rest_framework.permissions import BasePermission, SAFE_METHODS

from users import choices as user_choices
from . import models


class IsSellerOrReadOnly(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user
            and request.user.is_authenticated
            and request.user.user_type == user_choices.UserTypeChoices.Seller
        )


class IsSellerAndOwner(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_type == user_choices.UserTypeChoices.Seller
        )
    
    def has_object_permission(self, request, view, obj: models.SellerProduct):
        return obj.seller == request.user
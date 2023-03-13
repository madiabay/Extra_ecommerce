class ActionSerializerMixin:
    ACTION_SERIALIZERS = {}

    def get_serializer_class(self):
        return self.ACTION_SERIALIZERS.get(self.action, super().get_serializer_class())


class ActionPermissionMixin:
    ACTION_PERMISSIONS = {}

    def get_permissions(self):
        return self.ACTION_PERMISSIONS.get(self.action, super().get_permissions())
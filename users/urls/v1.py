from django.urls import path, include
from users.views import UserViewSet


urlpatterns = [
    path('users/create/', UserViewSet.as_view({'post': 'create_user'})),
    path('users/create-token/', UserViewSet.as_view({'post': 'create_token'})),
    path('users/', UserViewSet.as_view({'get': 'get_user'})),
]
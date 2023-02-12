from django.urls import path, include
from users.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('users/create/', UserViewSet.as_view({'post': 'create_user'})),
    path('users/verify/', UserViewSet.as_view({'post': 'verify_user'})),
    path('users/token/', UserViewSet.as_view({'post': 'create_token'})),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
from django.urls import path, include

urlpatterns = [
    path('', include('products.urls.v1')),
    path('', include('users.urls.v1')),
]

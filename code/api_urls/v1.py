from django.urls import path, include

urlpatterns = [
    path('', include('users.urls.v1')),
    path('', include('products.urls.v1')),
    path('', include('seller_products.urls.v1')),
    path('', include('orders.urls.v1')),
    path('', include('payments.urls.v1')),
]

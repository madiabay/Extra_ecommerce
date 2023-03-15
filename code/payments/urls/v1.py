from django.urls import path

from payments import views


urlpatterns = [
    path('bills/<bill_id>/pay/', views.BillViewSet.as_view({'post': 'pay_bill'}))
]
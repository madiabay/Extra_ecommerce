from rest_framework.routers import DefaultRouter

from orders import views


router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)

urlpatterns = router.urls
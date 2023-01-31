from rest_framework.routers import DefaultRouter

from products import views


router = DefaultRouter()
router.register(r'product-images', views.ProductImageViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = router.urls

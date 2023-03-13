from rest_framework.routers import DefaultRouter

from seller_products import views


router = DefaultRouter()
router.register(r'seller-products', views.SellerProductViewSet)

urlpatterns = router.urls
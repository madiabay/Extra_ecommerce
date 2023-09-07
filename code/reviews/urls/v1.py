from rest_framework.routers import DefaultRouter

from reviews import views


router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = router.urls

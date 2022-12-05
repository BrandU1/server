from rest_framework.routers import DefaultRouter

from .viewsets import BranduTossViewSet, BranduOrderViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduOrderViewSet, basename='order')
router.register('toss', BranduTossViewSet, basename='toss')

urlpatterns = router.urls

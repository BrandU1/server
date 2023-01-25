from rest_framework.routers import DefaultRouter

from .viewsets import (
    BranduTossViewSet, BranduOrderViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register('order', BranduOrderViewSet, basename='orders-order')
router.register('toss', BranduTossViewSet, basename='toss-payment')

urlpatterns = router.urls

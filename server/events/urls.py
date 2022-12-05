from rest_framework.routers import DefaultRouter

from events.viewsets import BranduCouponViewSet, BranduEventViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduEventViewSet, basename='event')
router.register('coupons', BranduCouponViewSet, basename='coupon')

urlpatterns = router.urls

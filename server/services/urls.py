from rest_framework.routers import DefaultRouter

from .viewsets import BranduServiceViewSet, BranduInquiryViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduServiceViewSet, basename='service')
router.register('inquiries', BranduInquiryViewSet, basename='inquiry')

urlpatterns = router.urls

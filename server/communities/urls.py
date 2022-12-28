from rest_framework.routers import DefaultRouter

from communities.viewsets.post import BranduPostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('post', BranduPostViewSet, basename='post')

urlpatterns = router.urls

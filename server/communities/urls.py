from rest_framework.routers import DefaultRouter

from communities.viewsets.comments import BranduCommentViewSet
from communities.viewsets.post import BranduPostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('posts', BranduPostViewSet, basename='post')
router.register('comments', BranduCommentViewSet, basename='comment')

urlpatterns = router.urls

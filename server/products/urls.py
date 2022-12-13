from rest_framework.routers import DefaultRouter

from .viewsets import BranduProductViewSet, BranduCategoryViewSet, BranduContentViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduProductViewSet, basename='product')
router.register('categories', BranduCategoryViewSet, basename='category')
router.register('contents', BranduContentViewSet, basename='content')

urlpatterns = router.urls

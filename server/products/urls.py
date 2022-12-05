from rest_framework.routers import DefaultRouter

from .viewsets import BranduProductViewSet, BranduCategoryViewSet, BranduContentBaseViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduProductViewSet, basename='product')
router.register('categories', BranduCategoryViewSet, basename='category')
router.register('contents', BranduContentBaseViewSet, basename='content')

urlpatterns = router.urls

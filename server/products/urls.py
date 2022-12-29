from rest_framework.routers import DefaultRouter

from .viewsets import BranduProductViewSet, BranduCategoryViewSet, BranduContentViewSet, BranduCustomViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduProductViewSet, basename='product')
router.register('categories', BranduCategoryViewSet, basename='category')
router.register('contents', BranduContentViewSet, basename='content')
router.register('customs', BranduCustomViewSet, basename='customs')

urlpatterns = router.urls

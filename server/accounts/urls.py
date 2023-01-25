from rest_framework.routers import DefaultRouter

from accounts.viewsets import (
    BranduProfileViewSet, BranduAddressViewSet, BranduReviewViewSet, BranduWishListViewSet, BranduBasketViewSet,
    BranduFollowViewSet, BranduCustomImageViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register('', BranduProfileViewSet, basename='profile')
router.register('addresses', BranduAddressViewSet, basename='address')
router.register('reviews', BranduReviewViewSet, basename='review')
router.register('wishes', BranduWishListViewSet, basename='wish')
router.register('baskets', BranduBasketViewSet, basename='basket')
router.register('follows', BranduFollowViewSet, basename='follow')
router.register('customs', BranduCustomImageViewSet, basename='custom')

urlpatterns = router.urls

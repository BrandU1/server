from rest_framework.routers import DefaultRouter

from accounts.views import (
    BranduProfileViewSet
)
from accounts.viewsets import (
    BranduAddressViewSet, BranduReviewViewSet, BranduWishListViewSet, BranduBasketViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register('', BranduProfileViewSet, basename='profile')
router.register('addresses', BranduAddressViewSet, basename='address')
router.register('reviews', BranduReviewViewSet, basename='review')
router.register('wishes', BranduWishListViewSet, basename='wish')
router.register('baskets', BranduBasketViewSet, basename='basket')

urlpatterns = router.urls
# [
# path('', include(router.urls)),
# path('notify/', NotifyAPIView.as_view()),
# path('summary/', ProfileSummaryAPIView.as_view()),
# path('scrapped/', PostScrappedListAPIView.as_view()),
# path('scrap/<int:pk>/', PostScrappedCreateAPIView.as_view()),
# path('<int:pk>/follows/', ProfileFollowListAPIView.as_view()),
# path('orders/', OrderListAPIView.as_view())
# ]

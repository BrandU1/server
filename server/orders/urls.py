from rest_framework.routers import DefaultRouter

from .viewsets import BranduOrderViewSet, BranduTossViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduOrderViewSet, basename='order')
router.register('toss', BranduTossViewSet, basename='toss')

urlpatterns = router.urls

# urlpatterns = [
#     path('toss/create/', OrderCreateAPIView.as_view()),
#     path('toss/confirm/', OrderTossConfirmAPIView.as_view()),
#     path('<int:pk>/', OrderAPIView.as_view()),
#     path('<int:pk>/tracking/', TrackingAPIView.as_view()),
#     path('<int:pk>/confirm/', OrderConfirmAPIView.as_view()),
# ]

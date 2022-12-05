from rest_framework.routers import DefaultRouter

from search.viewsets import BranduSearchViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduSearchViewSet, basename='search')

urlpatterns = router.urls

# urlpatterns = [
#     path('', SearchListAPIView.as_view()),
#     path('history/', SearchWordListAPIView.as_view()),
#     path('history/<int:pk>/', SearchWordDeleteAPIView.as_view()),
#     path('history/all/', SearchWordDeleteAllAPIView.as_view()),
#     path('rank/', SearchWordRankListAPIView.as_view()),
# ]

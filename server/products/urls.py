from rest_framework.routers import DefaultRouter

from .viewsets import BranduProductViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BranduProductViewSet, basename='product')

urlpatterns = router.urls

# urlpatterns = [
#     path('categories/', CategoryListView.as_view()),
#     path('category/<int:pk>/', ProductsByCategoryAPIView.as_view()),
#     path('category/sub/<int:pk>/', ProductCategoryListView.as_view()),
#     path('<int:pk>/', ProductRetrieveAPIView.as_view()),
#     path('<int:pk>/reviews/', ProductReviewListAPIView.as_view()),
#     path('hot-deal/', BranduHotDealListView.as_view()),
#     # path('<int:pk>/review/', ReviewCreateAPIView.as_view()),
# ]

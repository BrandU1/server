from django.urls import path
from .views import BranduHotDealListView, CategoryListView, ProductReviewListAPIView, ProductRetrieveAPIView, ReviewCreateAPIView


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('<int:pk>/', ProductRetrieveAPIView.as_view()),
    path('<int:pk>/reviews/', ProductReviewListAPIView.as_view()),
    path('hot-deal/', BranduHotDealListView.as_view()),
    path('<int:pk>/review/', ReviewCreateAPIView.as_view()),
]

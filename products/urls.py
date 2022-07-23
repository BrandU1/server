from django.urls import path
from .views import BranduHotDealListView, CategoryListView


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('hot-deal/', BranduHotDealListView.as_view()),
]

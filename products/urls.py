from django.urls import path
from .views import BranduHotDealListView


urlpatterns = [
    path('hot-deal/', BranduHotDealListView.as_view()),
]

from django.urls import path

from search.views import (
    SearchListAPIView, SearchWordListAPIView, SearchWordRankListAPIView, SearchWordDeleteAPIView,
    SearchWordDeleteAllAPIView
)

urlpatterns = [
    path('', SearchListAPIView.as_view()),
    path('history/', SearchWordListAPIView.as_view()),
    path('history/<int:pk>/', SearchWordDeleteAPIView.as_view()),
    path('history/all/', SearchWordDeleteAllAPIView.as_view()),
    path('rank/', SearchWordRankListAPIView.as_view()),
]

from django.urls import path

from search.views import SearchListAPIView, SearchWordListAPIView, SearchWordRankListAPIView

urlpatterns = [
    path('', SearchListAPIView.as_view()),
    path('history/', SearchWordListAPIView.as_view()),
    path('rank/', SearchWordRankListAPIView.as_view()),
]

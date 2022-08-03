from django.urls import path

from services.views import NoticeListAPIView

urlpatterns = [
    path('notice/', NoticeListAPIView.as_view()),
]

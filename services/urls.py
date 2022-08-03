from django.urls import path

from services.views import NoticeListAPIView, InquiryListCreateAPIView, InquiryUpdateAPIView, ServicesListAPIView

urlpatterns = [
    path('', ServicesListAPIView.as_view()),
    path('notice/', NoticeListAPIView.as_view()),
    path('inquiry/', InquiryListCreateAPIView.as_view()),
    path('inquiry/<int:pk>/', InquiryUpdateAPIView.as_view()),
]

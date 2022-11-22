from django.urls import path

from services.views import NoticeListAPIView, InquiryListCreateAPIView, InquiryRetrieveUpdateDestroyAPIView, ServicesListAPIView, FAQListAPIView, MainInfoListAPIVIew

urlpatterns = [
    path('', ServicesListAPIView.as_view()),
    path('notice/', NoticeListAPIView.as_view()),
    path('main-info/', MainInfoListAPIVIew.as_view()),
    path('faq/', FAQListAPIView.as_view()),
    path('inquiry/', InquiryListCreateAPIView.as_view()),
    path('inquiry/<int:pk>/', InquiryRetrieveUpdateDestroyAPIView.as_view()),
]

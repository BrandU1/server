from django.urls import path

from accounts.views import (
    ProfileDetailAPIView, ProfileFollowAPIView, ProfileEditAPIView, ProfileAPIView,
    AddressListAPIView, AddressEditAPIView, ReviewListAPIView, ReviewAPIView
)

urlpatterns = [
    path('me/', ProfileAPIView.as_view()),
    path('summary/', ProfileDetailAPIView.as_view()),
    path('follow/', ProfileFollowAPIView.as_view()),
    path('edit/', ProfileEditAPIView.as_view()),
    path('address/', AddressListAPIView.as_view()),
    path('address/<int:pk>/', AddressEditAPIView.as_view()),
    path('review/', ReviewListAPIView.as_view()),
    path('review/<int:pk>/', ReviewAPIView.as_view()),
]

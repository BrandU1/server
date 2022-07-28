from django.urls import path

from accounts.views import ProfileDetailAPIView, ProfileFollowAPIView, ProfileEditAPIView, AddressEditAPIView

urlpatterns = [
    path('summary/', ProfileDetailAPIView.as_view()),
    path('follow/', ProfileFollowAPIView.as_view()),
    path('edit/', ProfileEditAPIView.as_view()),
    path('address/', AddressEditAPIView.as_view()),
]

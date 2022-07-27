from django.urls import path

from accounts.views import ProfileDetailAPIView, ProfileFollowAPIView

urlpatterns = [
    path('me/', ProfileDetailAPIView.as_view()),
    path('follow/', ProfileFollowAPIView.as_view()),
]

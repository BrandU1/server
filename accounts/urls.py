from django.urls import path

from accounts.views import ProfileDetailAPIView

urlpatterns = [
    path('me/', ProfileDetailAPIView.as_view()),
]

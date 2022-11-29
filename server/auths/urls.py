from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import KakaoLoginAPI, NaverLoginAPI, GoogleLoginAPI, generate_token

urlpatterns = [
    path('kakao/login', KakaoLoginAPI.as_view()),
    path('naver/login', NaverLoginAPI.as_view()),
    path('google/login', GoogleLoginAPI.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('token', generate_token),
]

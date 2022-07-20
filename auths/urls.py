from django.urls import path

from .views import KakaoLoginAPI, KakaoCallbackAPI, NaverLoginAPI, NaverCallbackAPI, GoogleLoginAPI, GoogleSignInAPI

urlpatterns = [
    path('kakao/login/', KakaoLoginAPI.as_view()),
    path('kakao/callback/', KakaoCallbackAPI.as_view()),
    path('naver/login/', NaverLoginAPI.as_view()),
    path('naver/callback/', NaverCallbackAPI.as_view()),
    path('google/login/', GoogleLoginAPI.as_view()),
    path('google/callback/', GoogleSignInAPI.as_view()),
]

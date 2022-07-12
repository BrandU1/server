from django.urls import path

from .views import kakao_login_view, kakao_callback_view, google_login_view, google_sign_in_view


urlpatterns = [
    path('kakao/login/', kakao_login_view),
    path('kakao/callback/', kakao_callback_view),
    path('google/login/', google_login_view),
    path('google/callback/', google_sign_in_view),
]

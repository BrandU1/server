from django.urls import path

from events.views import CouponHoldListAPIView, CouponRegisterAPIView

urlpatterns = [
    path('coupons/', CouponHoldListAPIView.as_view()),
    path('coupons/register/', CouponRegisterAPIView.as_view()),
]

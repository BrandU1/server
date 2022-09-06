from django.urls import path

from events.views import (
    CouponHoldListAPIView, CouponRegisterAPIView, CarouselAdvertisementListAPIView, BannerAdvertisementListAPIView,

)

urlpatterns = [
    path('coupons/', CouponHoldListAPIView.as_view()),
    path('coupons/register/', CouponRegisterAPIView.as_view()),
    path('carousel/', CarouselAdvertisementListAPIView.as_view()),
    path('banner/', BannerAdvertisementListAPIView.as_view()),
]

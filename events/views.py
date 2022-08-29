from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from events.models import CouponHold, CouponNumber, Advertisement
from events.serializers import CouponHoldSerializer, AdvertisementSerializer


class CouponHoldListAPIView(ListAPIView):
    queryset = CouponHold.objects.all()
    serializer_class = CouponHoldSerializer

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        return self.queryset.filter(profile=profile.id)


class CouponRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)

        coupon_number = self.request.data.get('coupon_number', None)
        if coupon_number is None:
            raise Exception('')

        register_coupon = CouponNumber.objects.get(coupon_number=coupon_number)
        if register_coupon.is_use:
            raise Exception('')
        register_coupon.use_coupon()

        coupon = CouponHold.objects.create(
            profile=profile,
            coupon=register_coupon.coupon
        )

        serializer = CouponHoldSerializer(coupon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CarouselAdvertisementListAPIView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return self.queryset.filter(type='CAROUSEL')


class BannerAdvertisementListAPIView(ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        return self.queryset.filter(type='BANNER')

from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from events.models import CouponHold, CouponCoverage, Coupon, Advertisement
from products.serializers import ProductSimpleSerializer


class CouponCoverageSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(many=True)

    class Meta:
        model = CouponCoverage
        fields = ['product']


class CouponSerializer(serializers.ModelSerializer):
    coverage = CouponCoverageSerializer(source='couponcoverage_set', many=True)

    class Meta:
        model = Coupon
        fields = ['name', 'usable_period', 'expiration_period', 'coverage']


class CouponHoldSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer()

    class Meta:
        model = CouponHold
        fields = ['id', 'coupon', 'is_use', 'created']


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'backdrop_image', 'link']

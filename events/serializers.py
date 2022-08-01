from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from events.models import CouponHold, CouponCoverage, Coupon
from products.serializers import ProductSimpleSerializer


class CouponCoverageSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()

    class Meta:
        model = CouponCoverage
        fields = ['product']


class CouponSerializer(serializers.ModelSerializer):
    coverage = CouponCoverageSerializer(source='couponcoverage_set', many=True)

    class Meta:
        model = Coupon
        fields = ['name', 'usable_period', 'coverage']


class CouponHoldSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    coupon = CouponSerializer()

    class Meta:
        model = CouponHold
        fields = ['id', 'profile', 'coupon', 'is_use']

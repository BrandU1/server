from rest_framework import serializers

from accounts.models import Address, Profile, Point, Notify, Platform, Basket, WishList
from products.models import Review
from products.serializers import ProductSimpleSerializer


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    is_main = serializers.BooleanField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'is_main', 'name', 'recipient', 'address', 'road_name_address',
                  'detail_address', 'zip_code', 'phone_number', 'memo']

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        if not Address.objects.filter(profile=profile, is_main=True).exists():
            return Address.objects.create(profile=profile, **validated_data, is_main=True)
        return Address.objects.create(profile=profile, **validated_data)


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'memo', 'point', 'is_use', 'created']


class ProfilePointSerializer(serializers.ModelSerializer):
    point_history = PointSerializer(source='points', many=True)

    class Meta:
        model = Profile
        fields = ['point', 'point_history']


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = ['is_store', 'is_community', 'is_event']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['created', 'platform']


class WishListSerializer(serializers.ModelSerializer):
    is_basket = serializers.SerializerMethodField()
    product = ProductSimpleSerializer()

    class Meta:
        model = WishList
        fields = ['id', 'product', 'is_basket']

    def get_is_basket(self, obj):
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        profile = Profile.get_profile_or_exception(request.user.profile.id)
        return Basket.objects.filter(product_id=obj.product.pk, profile=profile).exists()


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'product', 'amount', 'is_purchase']


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'nickname', 'name']


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    profile_image = serializers.ImageField(use_url=True, read_only=True)
    nickname = serializers.CharField(allow_blank=True)
    name = serializers.CharField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True)
    social_link = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    platforms = PlatformSerializer(source='user.platform_set', many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'nickname', 'name', 'phone_number',
                  'email', 'social_link', 'description', 'platforms']


class ReviewListSerializer(serializers.ModelSerializer):
    profile = ProfileSimpleSerializer()

    class Meta:
        model = Review
        fields = ['id', 'profile', 'created', 'star', 'description']

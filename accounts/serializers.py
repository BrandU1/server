from rest_framework import serializers

from accounts.models import Address, Profile, Point, Notify, Platform, Basket, WishList
from products.models import Review, Product
from products.serializers import ProductSimpleSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'is_main', 'name', 'recipient', 'address', 'road_name_address',
                  'detail_address', 'zip_code', 'phone_number', 'memo']
        extra_kwargs = {
            'is_main': {'read_only': True}
        }

    def create(self, validated_data) -> Address:
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        if not Address.objects.filter(profile=profile, is_main=True).exists():
            return Address.objects.create(**validated_data, is_main=True)
        return Address.objects.create(**validated_data)


class AddressEditSerializer(AddressSerializer):
    class Meta(AddressSerializer.Meta):
        extra_kwargs = {
            'name': {'required': False},
            'recipient': {'required': False},
            'address': {'required': False},
            'road_name_address': {'required': False},
            'detail_address': {'required': False},
            'zip_code': {'required': False},
            'phone_number': {'required': False},
        }


class FollowingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'social_link']


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'memo', 'point', 'is_use', 'created']


class ProfilePointSerializer(serializers.ModelSerializer):
    point_history = PointSerializer(source='points', many=True)

    class Meta:
        model = Profile
        fields = ['point', 'point_history']


class ProfileSummarySerializer(serializers.ModelSerializer):
    pass


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
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Basket
        fields = ['product', 'product_id', 'amount', 'is_purchase']


class BasketPurchaseSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate(self, attrs):
        if not Product.objects.filter(pk=attrs['product']).exists():
            raise serializers.ValidationError("상품이 존재하지 않습니다.")

        profile_id = self.context.get("request").user.profile.id
        
        if not Basket.objects.filter(product_id=attrs['product'], profile_id=profile_id).exists():
            raise serializers.ValidationError("장바구니에 상품이 존재하지 않습니다.")

        return attrs


class ProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'nickname', 'name']


class ProfileSerializer(serializers.ModelSerializer):
    backdrop_image = serializers.ImageField(use_url=True, allow_empty_file=True)
    profile_image = serializers.ImageField(use_url=True, allow_empty_file=True)
    nickname = serializers.CharField(allow_blank=True)
    name = serializers.CharField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True)
    social_link = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    platforms = PlatformSerializer(source='user.platform_set', many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'backdrop_image', 'profile_image', 'nickname', 'name', 'phone_number',
                  'email', 'social_link', 'description', 'platforms']


class ReviewListSerializer(serializers.ModelSerializer):
    profile = ProfileSimpleSerializer()

    class Meta:
        model = Review
        fields = ['id', 'profile', 'created', 'star', 'description']

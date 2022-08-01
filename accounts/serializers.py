from rest_framework import serializers

from .models import Profile, Platform, Bucket, Address, Point
from products.serializers import ProductSimpleSerializer


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['created', 'platform']


class BucketSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()

    class Meta:
        model = Bucket
        fields = ['product', 'amount']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSummarySerializer(serializers.ModelSerializer):
    point = serializers.IntegerField(read_only=True)
    favorites = BucketSerializer(many=True)
    buckets = BucketSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['favorites', 'buckets', 'point']


class ProfileEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    platforms = PlatformSerializer(source='user.platform_set', many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'nickname', 'name', 'phone_number',
                  'email', 'social_link', 'description', 'platforms']


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'name', 'recipient', 'address', 'road_name_address', 'detail_address',
                  'priority', 'zip_code', 'phone_number', 'memo']

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
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

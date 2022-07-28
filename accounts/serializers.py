from rest_framework import serializers

from .models import Profile, Platform, Bucket, Address
from products.serializers import ProductSerializer


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['created', 'platform']


class BucketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Bucket
        fields = ['product', 'amount']


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


class AddressEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'road_name_address', 'detail_address', 'priority', 'zip_code', 'memo']

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        return Address.objects.create(profile=profile, **validated_data)

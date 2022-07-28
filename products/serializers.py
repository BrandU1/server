from rest_framework import serializers

from accounts.models import Profile
from .models import Product, MainCategory, SubCategory, Review


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'backdrop_image', 'name', 'price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    backdrop_image = serializers.ImageField(use_url=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'backdrop_image']


class MainCategorySerializer(serializers.ModelSerializer):
    backdrop_image = serializers.ImageField(use_url=True)
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'backdrop_image', 'color', 'sub_categories']


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'star', 'description']

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        return Review.objects.create(profile=profile, **validated_data)

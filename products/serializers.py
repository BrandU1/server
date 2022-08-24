from rest_framework import serializers

from accounts.models import Profile
from .models import Product, MainCategory, SubCategory, Review, Brand, ProductOption, Color


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    backdrop_image = serializers.ImageField(use_url=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'backdrop_image']


class MainCategorySerializer(serializers.ModelSerializer):
    backdrop_image = serializers.ImageField(use_url=True)
    sub_categories = SubCategorySerializer(source='subcategory_set', many=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'backdrop_image', 'color', 'sub_categories']


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'backdrop_image', 'name', 'price']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['name', 'hashcode']


class ProductOptionSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = ProductOption
        fields = ['id', 'color', 'size', 'count']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = SubCategorySerializer()
    options = ProductOptionSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    payment_day = serializers.CharField(read_only=True)
    is_write = serializers.BooleanField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product_name', 'payment_day', 'is_write',  'star', 'description']

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        return Review.objects.create(profile=profile, **validated_data)

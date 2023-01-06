from rest_framework import serializers

from accounts.models import Profile
from products.models import (
    Product, MainCategory, SubCategory, Review, Brand, ProductOption, Color, ProductImage,
    Content, HashTag, CustomProduct, CustomImage
)
from utils.remove import remove_background


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
    is_wish = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'backdrop_image', 'is_wish']

    def get_is_wish(self, obj) -> bool:
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        profile = Profile.get_profile_or_exception(request.user.profile.id)
        return profile.wishes.filter(id=obj.pk).exists()


class ProductHashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['kind', 'image']
        extra_kwargs = {
            'image': {'use_url': True},
        }


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
    brand = BrandSerializer()
    tags = ProductHashTagSerializer(many=True)
    images = ProductImageSerializer(many=True)
    options = ProductOptionSerializer(many=True)
    is_wish = serializers.SerializerMethodField()
    is_basket = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_is_wish(self, obj) -> bool:
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        profile = Profile.get_profile_or_exception(request.user.profile.id)
        return profile.wishes.filter(id=obj.pk).exists()

    def get_is_basket(self, obj) -> bool:
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        profile = Profile.get_profile_or_exception(request.user.profile.id)
        return profile.baskets.filter(id=obj.pk).exists()


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(source='order_product__product', read_only=True)
    product_name = serializers.CharField(source='order_product__product__name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'profile', 'order_product', 'product', 'product_name', 'created', 'star', 'comment']

    def validate_product(self, value):
        profile: Profile = self.context.get("profile", None)
        if not profile.orders.prefetch_related('products__product').filter(products__product=value).exists():
            raise serializers.ValidationError("해당 상품을 구매한 내역이 없습니다.")
        return value


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['title', 'url']


class CustomProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomProduct
        fields = ['id', 'product', 'profile', 'image']
        read_only_fields = ['profile']


class CustomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomImage
        fields = ['id', 'profile', 'image']
        read_only_fields = ['profile']

    def create(self, validated_data):
        image = validated_data.pop('image')
        profile = validated_data.pop('profile')
        new = remove_background(image, profile)
        instance = CustomImage.objects.create(profile=profile, image=new)
        return instance

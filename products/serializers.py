from rest_framework import serializers
from .models import Product, MainCategory, SubCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'backdrop_image', 'name', 'price']


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
        fields = ['id', 'name', 'backdrop_image', 'sub_categories']

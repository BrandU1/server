from django.contrib import admin

from .models import Product, MainCategory, SubCategory, Brand, Review, HashTag, Content, ProductImage, ProductOption, \
    Color, CustomImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ProductColorAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomImage)
class CustomImageAdmin(admin.ModelAdmin):
    pass

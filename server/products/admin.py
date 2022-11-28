from django.contrib import admin
from .models import Product, MainCategory, SubCategory, Brand, Review


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

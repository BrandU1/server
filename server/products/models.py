from django.conf import settings
from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.mixins import BaseModel


class Banner(models.Model):
    backdrop_image = models.ImageField(upload_to='banner', null=True, blank=True)


class Brand(models.Model):
    name = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='brand', null=True, blank=True)


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    # TODO: backgroundImage null 속성 제거
    backdrop_image = models.ImageField(upload_to='category', null=True, blank=True)
    color = models.CharField(max_length=10, default='#DDDDDD')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey('products.MainCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # TODO: backgroundImage null 속성 제거
    backdrop_image = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300)
    brand = models.ForeignKey('products.Brand', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('products.SubCategory', on_delete=models.CASCADE)
    backdrop_image = models.ImageField(upload_to='product/%Y-%m', null=True, blank=True)
    tags = models.ManyToManyField('products.HashTag', blank=True, related_name='products')
    price = models.IntegerField()

    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        cache.delete(f'product_{self.id}')

    def delete(self, using=None, keep_parents=False):
        cache.delete(f'product_{self.id}')
        super().delete(using, keep_parents)


class ProductViewCount(BaseModel):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='view_count')
    profile = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)


class HashTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    discount_price = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)


class ProductOption(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='options')
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE)
    size = models.CharField(max_length=4)
    count = models.IntegerField(default=0)


class Color(models.Model):
    name = models.CharField(max_length=20)
    hashcode = models.CharField(max_length=7)


class ProductImage(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images')
    kind = models.CharField(max_length=10)
    image = models.ImageField(upload_to='product/images/%Y-%m')


class Review(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True, related_name='reviews')
    order_product = models.OneToOneField('orders.OrderProduct', on_delete=models.CASCADE)
    star = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(null=True, blank=True)


class Content(models.Model):
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=50)

    @property
    def url(self):
        return f'{settings.BASE_BACKEND_URL}{self.path}'


class CustomProduct(BaseModel):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='custom_products')
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='custom_products')
    image = models.ImageField(upload_to='custom_product/%Y-%m', null=True)


class CustomImage(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='custom_images')
    image = models.ImageField(upload_to='custom_product/%Y-%m', null=True)

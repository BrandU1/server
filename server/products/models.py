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
    price = models.IntegerField()


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


class ProductImages(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    kind = models.CharField(max_length=10)
    image = models.ImageField(upload_to='product/images/%Y-%m')


class Review(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    order_product = models.OneToOneField('orders.OrderProduct', on_delete=models.CASCADE)
    star = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.TextField(null=True, blank=True)
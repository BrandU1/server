from datetime import datetime
from random import randint

from django.db import models

from core.mixins import BaseModel
from products.models import Review


def generate_order_number():
    now = datetime.now()
    year = now.year
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    random_number = str(randint(1, 100000)).zfill(6)
    return f'{year}{month}-{day}{hour}{minute}-{random_number}'


class Order(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    address = models.ForeignKey('accounts.Address', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    coupon = models.ForeignKey('events.CouponHold', on_delete=models.CASCADE, null=True)
    used_point = models.IntegerField(default=0)
    price = models.IntegerField()
    status = models.CharField(max_length=10, default='paid')
    method = models.CharField(max_length=20)
    is_confirm = models.BooleanField(default=False)

    def confirm_order(self, platform: str, price: int, name: str, payment_key: str, method: str):
        self.is_confirm = True
        self.save()
        return Payment.objects.create(
            order=self,
            platform=platform,
            price=price,
            name=name,
            payment_key=payment_key,
            method=method
        )

    @property
    def is_confirmed(self):
        return self.status == 'confirm'


class OrderProduct(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)
    option = models.ForeignKey('products.ProductOption', on_delete=models.SET_NULL, null=True)
    discount = models.ForeignKey('products.Discount', on_delete=models.SET_NULL, null=True)


class Payment(BaseModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    platform = models.CharField(max_length=30)
    price = models.IntegerField()
    name = models.CharField(max_length=200)
    payment_key = models.CharField(max_length=50)
    method = models.CharField(max_length=10)


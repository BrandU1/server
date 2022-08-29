from django.db import models

from core.mixins import BaseModel


class Coupon(models.Model):
    name = models.CharField(max_length=100)
    usable_period = models.DateTimeField()
    expiration_period = models.IntegerField()


class CouponNumber(models.Model):
    coupon = models.ForeignKey('events.Coupon', on_delete=models.CASCADE)
    coupon_number = models.CharField(max_length=30)
    is_use = models.BooleanField(default=False)

    def use_coupon(self) -> None:
        self.is_use = True
        self.save()

    def __str__(self):
        return f'{self.coupon.name}: {self.coupon_number}'


class CouponCoverage(models.Model):
    coupon = models.ForeignKey('events.Coupon', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)


class CouponHold(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    coupon = models.ForeignKey('events.Coupon', on_delete=models.CASCADE)
    is_use = models.BooleanField(default=False)


class Advertisement(BaseModel):
    type = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    backdrop_image = models.ImageField(upload_to='events/banner')
    link = models.URLField()

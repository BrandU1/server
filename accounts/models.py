from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, Deferrable

from core.mixins import BaseMixins


class User(AbstractUser):
    pass


class Platform(BaseMixins, models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    platform = models.CharField(max_length=10)
    platform_id = models.CharField(max_length=30)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['platform', 'platform_id'], name='unique_platform_id',
                             deferrable=Deferrable.DEFERRED),
        ]


class Profile(BaseMixins, models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='media/%Y/%m/%d')
    nickname = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)
    description = models.TextField()
    bucket = models.ManyToManyField('products.Product', through='accounts.Bucket',
                                    through_fields=('profile', 'product'))
    following = models.ManyToManyField('accounts.Profile', related_name='+')
    follower = models.ManyToManyField('accounts.Profile', related_name='+')


class Address(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    road_name_address = models.CharField(max_length=200)
    detail_address = models.CharField(max_length=100)
    priority = models.SmallIntegerField(default=1)
    zip_code = models.CharField(max_length=5)
    memo = models.TextField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['profile', 'priority'], name='unique_priority', deferrable=Deferrable.DEFERRED),
        ]


class Point(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    point = models.IntegerField()
    memo = models.CharField(max_length=200)


class Bucket(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='+')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_purchase = models.BooleanField(default=False)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, Deferrable

from server.mixins import BaseMixins


class User(AbstractUser):
    platform = models.CharField(max_length=50)


class Profile(BaseMixins, models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='media/%Y/%m/%d')
    nickname = models.CharField(max_length=100, null=True)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)

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


# TODO: Bucket List
# class Bucket(BaseMixins, models.Model):
#     profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
#     custom_product = models.ForeignKey('Product')
#
#     amount = models.IntegerField()
#     is_purchase = models.BooleanField(default=False)

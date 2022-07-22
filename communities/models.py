from django.db import models

from core.mixins import BaseMixins


class Post(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)


class Review(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)

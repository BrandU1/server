from django.db import models

from server.mixins import BaseMixins


class Post(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)


class Review(BaseMixins, models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)

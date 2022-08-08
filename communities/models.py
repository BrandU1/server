from django.db import models

from core.mixins import BaseModel


class Post(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)


class Review(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)

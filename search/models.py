from django.db import models

from core.mixins import BaseModel


class Search(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    search_word = models.CharField(max_length=100)

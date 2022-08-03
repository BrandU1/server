from django.db import models

from core.mixins import BaseModel


class Notice(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()

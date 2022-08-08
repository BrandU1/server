from django.db import models

from core.managers import CustomModelManager


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    not_deleted = CustomModelManager()

    class Meta:
        abstract = True

from django.db import models


class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super(CustomModelManager, self).get_queryset().filter(is_deleted=False)

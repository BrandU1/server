from datetime import datetime

from django.db import models


class DjangoException(models.Model):
    status_code = models.Model


class OrderNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(self, *args, **kwargs)

    @classmethod
    def generate_order_number(cls):
        year = datetime.now().year
        return year

from django.db import models

from core.mixins import BaseModel


class Order(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('accounts.Address', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    price = models.IntegerField()
    status = models.CharField(max_length=10, default='PENDING')
    is_confirmed = models.BooleanField(default=False)

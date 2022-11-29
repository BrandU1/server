import os
from datetime import datetime
from random import randint

import requests
from django.db import models

from core.mixins import BaseModel


def generate_order_number():
    now = datetime.now()
    year = now.year
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    random_number = str(randint(1, 100000)).zfill(6)
    return f'{year}{month}-{day}{hour}{minute}-{random_number}'


class Order(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    coupon = models.ForeignKey('events.CouponHold', on_delete=models.CASCADE, null=True)
    used_point = models.IntegerField(default=0)
    price = models.IntegerField()
    method = models.CharField(max_length=20)
    is_payment_confirm = models.BooleanField(default=False)
    is_confirm = models.BooleanField(default=False)

    def confirm_payment(self, platform: str, price: int, name: str, payment_key: str, method: str):
        self.is_payment_confirm = True
        self.save()
        delivery = Delivery.objects.create(
            order=self,
            invoice_number=''
        )
        return Payment.objects.create(
            order=self,
            platform=platform,
            price=price,
            name=name,
            payment_key=payment_key,
            method=method
        )

    def confirm_order(self) -> None:
        self.is_confirm = True
        self.save()

    @property
    def status(self):
        if self.is_confirm:
            return 'confirm'
        return self.delivery.status


class OrderProduct(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)
    option = models.ForeignKey('products.ProductOption', on_delete=models.SET_NULL, null=True)
    discount = models.ForeignKey('products.Discount', on_delete=models.SET_NULL, null=True)


class Payment(BaseModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    platform = models.CharField(max_length=30)
    price = models.IntegerField()
    name = models.CharField(max_length=200)
    payment_key = models.CharField(max_length=50)
    method = models.CharField(max_length=10)


class Delivery(BaseModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery')
    invoice_number = models.CharField(max_length=30, null=True)
    courier_code = models.CharField(max_length=3, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def update_courier_code(self) -> None:
        response = requests.get('https://info.sweettracker.co.kr/api/v1/recommend', headers={
            'accept': 'application/json'
        }, params={
            't_key': os.environ.get('SMART_TRACKER'),
            't_invoice': self.invoice_number,
        })

        if response.status_code == 200:
            data = response.json()
            for courier in data['Recommend']:
                code = courier['Code']
                is_result = False
                try:
                    self.update_tracking(courier_code=code)
                    is_result = True
                finally:
                    if is_result:
                        self.courier_code = code
                        self.save()
                        return
        raise Exception('일치하는 코드가 존재하지 않습니다.')

    def update_tracking(self, courier_code: str = '00') -> None:
        if self.is_done:
            return
        code = courier_code if courier_code != '00' else self.courier_code
        response = requests.get('https://info.sweettracker.co.kr/api/v1/trackingInfo', headers={
            'accept': 'application/json'
        }, params={
            't_key': os.environ.get('SMART_TRACKER'),
            't_code': code,
            't_invoice': self.invoice_number,
        })
        if response.status_code == 200:
            data = response.json()
            tracking_lists = data['trackingDetails']
            for tracking in tracking_lists:
                self.tracking.get_or_create(
                    delivery=self,
                    datetime=datetime.strptime(tracking['timeString'], '%Y-%m-%d %H:%M:%S'),
                    level=tracking['level'],
                    kind=tracking['kind'],
                    place=tracking['where'],
                    phone_number=tracking['telno']
                )
            self.save()
            return
        raise Exception('')

    @property
    def status(self):
        if self.tracking.count() == 0:
            return 'paid'
        if self.tracking.last().level == 6:
            return 'complete'
        return 'delivery'


class DeliveryTracking(models.Model):
    delivery = models.ForeignKey('orders.Delivery', on_delete=models.CASCADE, related_name='tracking')
    datetime = models.DateTimeField()
    kind = models.CharField(max_length=30)
    level = models.IntegerField()
    place = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)

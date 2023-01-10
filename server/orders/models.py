import base64
import json
import os
from datetime import datetime
from random import randint

import requests
from django.db import models

from core.exceptions.order import OrderAlreadyConfirmException, OrderPaymentAlreadyConfirmException, \
    OrderPaymentPriceNotEqualException, TossPaymentException
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


def encrypt_secret_key(key: str):
    bytes_key = key.encode('UTF-8')
    base64_bytes = base64.b64encode(bytes_key)
    return base64_bytes.decode('UTF-8')


class Order(BaseModel):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=30)
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    coupon = models.ForeignKey('events.CouponHold', on_delete=models.CASCADE, blank=True, null=True)
    used_point = models.IntegerField(default=0)
    price = models.IntegerField()
    method = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20, default='결제 대기')
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

    def toss_payment_create(self, payment_key: str, order_id: str, amount: int):
        if self.is_payment_confirm:
            raise OrderPaymentAlreadyConfirmException()

        if self.price != int(amount):
            raise OrderPaymentPriceNotEqualException()
        request = requests.post(
            'https://api.tosspayments.com/v1/payments/confirm',
            headers={
                'Authorization': f'Basic {encrypt_secret_key(os.environ.get("TOSSPAYMENT_SECRET_KEY"))}',
                'Content-Type': 'application/json',
            }, data=json.dumps({
                'paymentKey': payment_key,
                'orderId': order_id,
                'amount': amount,
            })
        )

        if request.status_code != 200:
            error = request.json()
            raise TossPaymentException(
                status_code=request.status_code,
                message=error.get('message'),
                code=error.get('code')
            )

        data = request.json()
        self.is_payment_confirm = True
        delivery = Delivery.objects.create(
            order=self,
            invoice_number=''
        )
        return Payment.objects.create(
            order=self,
            platform='TOSS',
            price=amount,
            name=data.get('name', self.name),
            payment_key=payment_key,
            method=data.get('method', self.method),
            recipient_url=data.get('receipt').get('url')
        )

    def confirm_order(self) -> None:
        if self.is_confirm:
            raise OrderAlreadyConfirmException()
        self.is_confirm = True
        self.save(update_fields=['is_confirm'])

    @property
    def status(self):
        if self.is_confirm:
            return 'confirm'
        return self.delivery.status

    def __str__(self):
        return f'{self.name}/{self.order_number}'


class OrderProduct(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)
    option = models.ForeignKey('products.ProductOption', on_delete=models.SET_NULL, blank=True, null=True)
    discount = models.ForeignKey('products.Discount', on_delete=models.SET_NULL, blank=True, null=True)
    is_review_written = models.BooleanField(default=False)


class Payment(BaseModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    platform = models.CharField(max_length=30)
    price = models.IntegerField()
    name = models.CharField(max_length=200)
    payment_key = models.CharField(max_length=50)
    recipient_url = models.URLField()
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

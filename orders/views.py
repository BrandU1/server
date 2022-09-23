import json
import os
from datetime import datetime, timedelta

import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

import base64
from core.permissions import IsAuthor
from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderSerializer, PaymentSerializer, DeliverySerializer


class OrderCreateAPIView(APIView):
    @swagger_auto_schema(request_body=OrderCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                'order_number': order.order_number
            }, status=status.HTTP_201_CREATED)
        raise Exception(serializer.errors)


class OrderTossConfirmAPIView(APIView):
    permission_classes = [IsAuthor]

    def get_object(self, order_number):
        order = Order.objects.get(order_number=order_number)
        self.check_object_permissions(self.request, order)
        return order

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'paymentKey': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'orderId': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'amount': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def post(self, request, *args, **kwargs):
        payment_key = self.request.data['paymentKey']
        order_id = self.request.data['orderId']
        amount = self.request.data['amount']
        order = self.get_object(order_number=order_id)
        if order.is_confirm:
            raise Exception('이미 처리된 결제입니다.')

        if order.price == int(amount):
            request = requests.post('https://api.tosspayments.com/v1/payments/confirm', headers={
                'Authorization': f'Basic {os.environ.get("TOSSPAYMENT_API_KEY")}',
                'Content-Type': 'application/json',
            }, data=json.dumps(self.request.data))
            if request.status_code == 200:
                data = request.json()
                payment = order.confirm_order(
                    platform='TOSS',
                    price=int(data['totalAmount']),
                    name=data['orderName'],
                    payment_key=payment_key,
                    method=data['method']
                )
                serializer = PaymentSerializer(payment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise Exception(request.json())
        raise Exception('요청하신 금액과 다릅니다.')


class OrderTossCancelAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        order = Order.objects.get(id=pk)
        return Response()


class OrderAPIView(APIView):
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        order = Order.objects.get(pk=pk)
        self.check_object_permissions(self.request, order)
        return order

    @swagger_auto_schema(responses={200: OrderSerializer()})
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception()
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={204: ''})
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception()
        order = self.get_object(pk)
        order.is_deleted = True
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrackingAPIView(APIView):
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        order = Order.objects.get(pk=pk)
        self.check_object_permissions(self.request, order)
        return order

    def get(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise Exception('')
        order = self.get_object(pk=pk)
        delivery = order.delivery
        if delivery.courier_code is None:
            delivery.update_courier_code()
        if delivery.updated < timezone.now() - timedelta(hours=2):
            delivery.update_tracking()

        serializer = DeliverySerializer(delivery)
        return Response(serializer.data, status=status.HTTP_200_OK)


import os

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from core.permissions import IsAuthor
from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderSerializer


class OrderCreateAPIView(APIView):
    @swagger_auto_schema(request_body=OrderCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            order = serializer.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderTossConfirmAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payment_key = self.request.data['payment_key']
        order_id = self.request.data['order_id']
        amount = self.request.data['amount']
        order = get_object_or_404(Order, order_number=order_id)
        if order.price == amount:
            request = requests.post('https://api.tosspayments.com/v1/payments/confirm', headers={
                'Authorization': f'Basic {os.environ.get("TOSSPAYMENT_SECRET_KEY")}'
            }, data={
                'paymentKey': payment_key,
                'orderId': order_id,
                'amount': amount
            })
            print(request.json())
            return Response(status=status.HTTP_200_OK)
        raise Exception('')


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

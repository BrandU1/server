from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from core.permissions import IsAuthor
from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderSerializer


class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        orders = Order.objects.filter(profile=profile)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=OrderCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

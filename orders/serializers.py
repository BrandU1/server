from rest_framework import serializers

from accounts.serializers import ProfileSerializer, AddressSerializer
from orders.models import Order
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    product = ProductSerializer()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    order_number = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['product', 'address', 'price', 'order_number']

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Profile, Address
from accounts.serializers import ProfileSerializer, AddressSerializer
from orders.models import Order, OrderProduct, Payment
from products.serializers import ProductSerializer, ProductSimpleSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'count', 'option', 'discount']


class OrderProductSimpleSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'count', 'option', 'discount']


class OrderCreateSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    coupon = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = ['name', 'address', 'products', 'price', 'coupon', 'used_point', 'method']

    def validate_address(self, address):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        if address.profile == profile:
            return address
        raise ValidationError('자기 자신의 주소지가 들어가야합니다.')

    def create(self, validated_data: dict) -> Order:
        products = validated_data.pop('products')
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        order = Order.objects.create(profile=profile, **validated_data)
        order.products.set([OrderProduct.objects.create(order=order, **product) for product in products])
        return order


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSimpleSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = '__all__'

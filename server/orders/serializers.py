from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Profile
from accounts.serializers import AddressSerializer
from orders.models import Order, OrderProduct, Payment, Delivery, DeliveryTracking


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'count', 'created']
        extra_kwargs = {
            'created': {'read_only': True},
        }


class OrderCreateSerializer(serializers.ModelSerializer):
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
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'products', 'address', 'created', 'name', 'order_number',
                  'status', 'used_point', 'price', 'method', 'is_confirm', 'is_payment_confirm', 'coupon']


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class DeliveryTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTracking
        fields = ['datetime', 'level', 'kind', 'place', 'phone_number']


class DeliverySerializer(serializers.ModelSerializer):
    tracking = DeliveryTrackingSerializer(many=True)

    class Meta:
        model = Delivery
        fields = ['id', 'order', 'status', 'invoice_number', 'is_done', 'tracking']

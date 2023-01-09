from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Profile, Basket
from accounts.serializers import AddressSerializer
from orders.models import Order, OrderProduct, Payment, Delivery, DeliveryTracking
from products.models import Product
from products.serializers import ProductSimpleSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='order_product_id', read_only=True)
    order = serializers.IntegerField(source='id', read_only=True)
    product = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField()

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'count', 'created']


class OrderProductsSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    count = serializers.IntegerField()

    def validate(self, attrs):
        if not Product.objects.filter(pk=attrs['product']).exists():
            raise serializers.ValidationError("상품이 존재하지 않습니다.")

        if not Basket.objects.filter(
                custom_product__product_id=attrs['product'],
                profile=self.context['profile']
        ).exists():
            raise serializers.ValidationError("장바구니에 상품이 존재하지 않습니다.")
        return attrs


class OrderCreateSerializer(serializers.ModelSerializer):
    coupon = serializers.IntegerField(required=False, allow_null=True)
    products = OrderProductsSerializer(many=True)

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
        order = Order.objects.create(profile=self.context.get('profile'), **validated_data)
        order.products.set([OrderProduct.objects.create(
            order=order, product_id=product['product'], count=product['count']
        ) for product in products])
        return order


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    products = ProductSimpleSerializer(many=True)

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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from core.exceptions.order import OrderPaymentAlreadyConfirmException, OrderPaymentPriceNotEqualException, \
    TossPaymentException
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from orders.models import Order
from orders.serializers import OrderSerializer, PaymentSerializer, OrderCreateSerializer


class BranduTossViewSet(BranduBaseViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthor]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'confirm':
            return PaymentSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            response = {
                'order_number': order.order_number,
            }

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'paymentKey': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'orderId': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'amount': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    @action(detail=False, methods=['POST'])
    def confirm(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        payment_key = self.request.data['paymentKey']
        order_id = self.request.data['orderId']
        amount = self.request.data['amount']

        try:
            order = get_object_or_404(Order, order_number=order_id)
            payment = order.toss_payment_create(
                payment_key=payment_key,
                amount=amount,
                order_id=order_id,
            )
            serializer = self.get_serializer_class()(payment)
            response = serializer.data

        except OrderPaymentAlreadyConfirmException as e:
            is_success = False
            status_code = e.status_code
            response = {
                'code': e.default_code,
                'message': e.default_detail,
            }

        except OrderPaymentPriceNotEqualException as e:
            is_success = False
            status_code = e.status_code
            response = {
                'code': e.default_code,
                'message': e.default_detail,
            }

        except TossPaymentException as e:
            is_success = False
            status_code = e.status_code
            response = {
                'code': e.default_code,
                'message': e.default_detail,
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

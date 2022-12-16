from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from core.exceptions.order import OrderAlreadyConfirmException
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from orders.models import Order
from orders.serializers import OrderSerializer, OrderCreateSerializer


class BranduOrderViewSet(BranduBaseViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthor]
    login_required = True

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            response = {
                'order_number': order.order_number
            }

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'message': str(e)
            }
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        order = self.get_object()
        serializer = self.get_serializer(order)
        response = serializer.data
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def destroy(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True
        order = self.get_object()
        self.perform_destroy(order)
        response = {}
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=['PATCH'])
    def confirm(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            order = self.get_object()
            order.confirm()
            serializer = self.get_serializer(order)
            response = serializer.data

        except OrderAlreadyConfirmException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': 400,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @swagger_auto_schema(request_body=no_body, deprecated=True)
    @action(detail=True, methods=['GET'])
    def tracking(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            order = self.get_object()
            order.tracking()
            serializer = self.get_serializer(order)
            response = serializer.data

        except OrderAlreadyConfirmException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': 400,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

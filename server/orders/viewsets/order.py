from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from core.exceptions.order import OrderAlreadyConfirmException
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from orders.models import Order
from orders.serializers import OrderSerializer


class BranduOrderViewSet(BranduBaseViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    login_required = False

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

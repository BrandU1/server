from django.db.models import Count, F, Subquery
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

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        order = Order.objects.filter(id=pk).annotate(
            recipient=F('address__recipient'),
            phone_number=F('address__phone_number'),
            detail_address=F('address__detail_address'),
            zip_code=F('address__zip_code'),
            road_address=F('address__address'),
        ).values(
            'id', 'order_number', 'created', 'recipient', 'phone_number', 'detail_address', 'zip_code',
            'road_address', 'price', 'used_point'
        ).first()
        products = Order.objects.prefetch_related(
                    'products__product',
                ).annotate(
                    product_id=F('products__product__id'),
                    product_name=F('products__product__name'),
                    product_image=F('products__product__backdrop_image'),
                    product_price=F('products__product__price'),
                ).values(
                    'product_id', 'product_name', 'product_image', 'product_price',
                ).filter(
                    id=pk,
                ).annotate(
                    id=F('product_id'),
                    name=F('product_name'),
                    backdrop_image=F('product_image'),
                    price=F('product_price'),
                ).values(
                   'id', 'name', 'backdrop_image', 'price'
                )
        response = {
            'order': order,
            'products': products,
        }

        # serializer = self.get_serializer(order)
        # response = serializer.data
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

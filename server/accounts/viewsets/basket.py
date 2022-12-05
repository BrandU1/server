from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from accounts.models import Basket
from accounts.serializers import BasketSerializer, BasketPurchaseSerializer
from core.exceptions.product import RelationAlreadyExistException, RelationDoesNotExistException
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Product


class BranduBasketViewSet(BranduBaseViewSet):
    model = Basket
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    @staticmethod
    def get_product(pk=None):
        return get_object_or_404(Product, pk=pk)

    def list(self, request, *args, **kwargs):
        """ 장바구니 목록 조회 API """
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            baskets = self.get_queryset()
            serializer = self.serializer_class(baskets, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @swagger_auto_schema(request_body=no_body)
    @action(detail=False, methods=['POST'], url_path='(?P<pk>[0-9]+)')
    def create_basket(self, request, pk=None, *args, **kwargs):
        """ 장바구니 추가 API """
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            product = self.get_product(pk=pk)
            Basket.add(profile=self.profile, product=product)
            response = {
                'message': '장바구니에 추가되었습니다.'
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        except RelationAlreadyExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @create_basket.mapping.delete
    def destroy(self, request, pk=None, *args, **kwargs):
        """ 장바구니 삭제 API """
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            product = self.get_product(pk=pk)
            Basket.remove(profile=self.profile, product=product)
            response = {}

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        except RelationDoesNotExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['GET'], detail=False, url_path='purchase', description='장바구니 구매 내역 조회 API')
    def purchase_list(self, request, *args, **kwargs):
        """ 장바구니 구매 내역 조회 API """
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            baskets = self.get_queryset().filter(is_purchase=True)
            serializer = self.serializer_class(baskets, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @swagger_auto_schema(request_body=BasketPurchaseSerializer(many=True))
    @purchase_list.mapping.patch
    def purchase_create(self, request, *args, **kwargs):
        """ 장바구니 구매 API """
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = BasketPurchaseSerializer(data=request.data, many=True, context={'profile': self.profile})
            serializer.is_valid(raise_exception=True)

            for data in serializer.validated_data:
                product = self.get_product(pk=data['product'])
                basket = Basket.objects.get(profile=self.profile, product=product)
                basket.purchase(amount=data['amount'])

            response = {
                'message': '구매가 처리가 완료되었습니다.'
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

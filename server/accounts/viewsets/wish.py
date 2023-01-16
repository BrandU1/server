from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from accounts.models import WishList
from accounts.serializers import WishListSerializer
from core.exceptions.product import RelationAlreadyExistException, RelationDoesNotExistException
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Product


class BranduWishListViewSet(BranduBaseViewSet):
    model = WishList
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    @staticmethod
    def get_product(pk=None):
        return get_object_or_404(Product, pk=pk)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=['POST'], detail=False, url_path='(?P<pk>[0-9]+)', description='사용자 위시 리스트 추가')
    def create_with_pk(self, request, pk=None, *args, **kwargs):
        """사용자 위시 리스트 생성 API"""
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            product = self.get_product(pk=pk)
            WishList.add(profile=self.profile, product=product)
            response = {
                'message': '위시 리스트에 추가되었습니다.'
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'error': str(e)
            }

        except RelationAlreadyExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'error': str(e.detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @create_with_pk.mapping.delete
    def destroy_with_pk(self, request, pk=None, *args, **kwargs):
        """사용자 위시 리스트 삭제 API"""
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            product = self.get_product(pk=pk)
            WishList.remove(profile=self.profile, product=product)
            response = {
                'message': '위시 리스트에서 삭제되었습니다.'
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'error': str(e)
            }

        except RelationDoesNotExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'error': str(e.detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

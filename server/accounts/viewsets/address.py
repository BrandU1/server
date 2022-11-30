from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated

from accounts.models import Address
from accounts.serializers import AddressSerializer, AddressEditSerializer
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


class BranduAddressViewSet(BranduBaseViewSet):
    model = Address
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = AddressSerializer
    login_required = True

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AddressEditSerializer
        return self.serializer_class

    # 사용자 주소 디테일 조회 API
    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            address = self.get_object()
            serializer = self.serializer_class(address)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 주소 목록 조회 API
    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            addresses = self.get_queryset().values(
                'id', 'is_main', 'name', 'recipient', 'address', 'road_name_address',
                'detail_address', 'zip_code', 'phone_number', 'memo',
            )
            serializer = self.serializer_class(addresses, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 주소 데이터 생성 API
    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = serializer.data

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 주소 데이터 수정 API
    def partial_update(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            address = self.get_object()
            serializer = self.serializer_class(address, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e)
            }

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 주소 데이터 삭제 API
    def destroy(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            address = self.get_object()
            self.perform_destroy(address)
            response = {
                'message': '주소가 삭제되었습니다.'
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 기본 배송지 설정 API
    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=['POST'], description='사용자 기본 배송지 설정')
    def main(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        address: Address = self.get_object()
        address.set_main()
        serializer = self.serializer_class(address)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

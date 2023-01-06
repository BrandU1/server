from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import CustomProduct
from products.serializers import CustomProductSerializer


class BranduCustomViewSet(BranduBaseViewSet):
    model = CustomProduct
    queryset = CustomProduct.objects.all()
    serializer_class = CustomProductSerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = serializer.data

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        serializer = self.serializer_class(self.get_queryset(), many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def retrieve(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        serializer = self.serializer_class(self.get_object())
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def destroy(self, request, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        self.perform_destroy(self.get_object())

        return brandu_standard_response(is_success=is_success, response={}, status_code=status_code)

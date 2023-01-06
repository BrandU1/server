from rest_framework import status
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

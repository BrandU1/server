from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import CustomProduct
from products.serializers import CustomProductSerializer, CustomImageSerializer


class BranduCustomViewSet(BranduBaseViewSet):
    model = CustomProduct
    queryset = CustomProduct.objects.all()
    serializer_class = CustomProductSerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny], url_path='remove',
            serializer_class=CustomImageSerializer)
    def remove_background(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
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

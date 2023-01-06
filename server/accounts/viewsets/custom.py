from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import CustomImage
from products.serializers import CustomImageSerializer


class BranduCustomImageViewSet(BranduBaseViewSet):
    model = CustomImage
    queryset = CustomImage.objects.all()
    serializer_class = CustomImageSerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(profile=self.profile)
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

from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from services.models import Inquiry
from services.serializers import InquirySerializer


class BranduInquiryViewSet(BranduBaseViewSet):
    model = Inquiry
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            inquiries = self.get_queryset()
            serializer = self.get_serializer(inquiries, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(profile=self.profile)
            response = serializer.data

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        inquiry = self.get_object()
        serializer = self.serializer_class(inquiry)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def partial_update(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            inquiry = self.get_object()
            serializer = self.serializer_class(inquiry, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def destroy(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            inquiry = self.get_object()
            self.perform_destroy(inquiry)
            response = {
                'message': 'Inquiry deleted successfully'
            }

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

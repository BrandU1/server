from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Review
from products.serializers import ReviewSerializer


class BranduReviewViewSet(BranduBaseViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    login_required = True

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [*permission_classes, IsAuthor]
        return [permission() for permission in permission_classes]

    # 사용자 리뷰 목록 조회 API
    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            reviews = self.get_queryset()
            serializer = self.serializer_class(reviews, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'error': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 리뷰 수정 API
    def partial_update(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            review = self.get_object()
            serializer = self.serializer_class(review, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'error': str(e)
            }

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'error': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 리뷰 삭제 API
    def destroy(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            review = self.get_object()
            self.perform_destroy(review)
            response = {
                'message': '리뷰가 삭제되었습니다.'
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'error': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

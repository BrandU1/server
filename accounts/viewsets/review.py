from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Review
from products.serializers import ReviewSerializer


class BranduReviewViewSet(BranduBaseViewSet):
    model = Review
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
            reviews = self.get_queryset().annotate(
                product_name=F('product__name'),
                payment_day=F('order__created'),
            ).values(
                'id', 'product_name', 'payment_day', 'star', 'description'
            )
            serializer = self.serializer_class(reviews, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 작성 가능 리뷰 목록 조회 API
    @action(detail=False, methods=['GET'], url_path='writable')
    def writable_reviews(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            self.profile.orders.prefetch_related('products')

            reviews = self.get_queryset().filter(user=request.user, is_writable=True)
            serializer = self.serializer_class(reviews, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 사용자 리뷰 생성 API
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
                'message': str(e.default_detail)
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
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.status_code)
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
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

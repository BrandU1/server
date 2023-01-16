from datetime import date

from django.core.cache import cache
from django.db.models import F, Subquery
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny

from accounts.models import Basket
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from orders.models import OrderProduct
from products.models import Product, ProductViewCount, Review, MainCategory, Content, CustomProduct
from products.serializers import ProductSerializer, ReviewSerializer, ContentSerializer, MainCategorySerializer, \
    CustomProductSerializer


class BranduProductViewSet(BranduBaseViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    login_required = False

    def get_serializer_class(self):
        if self.action == 'contents':
            return ContentSerializer
        return self.serializer_class

    def update_view_count(self, product) -> int:
        try:
            if self.profile:
                ProductViewCount.objects.get_or_create(
                    profile=self.profile,
                    product=product,
                    created__date=date.today()
                )

        except PermissionDenied:
            pass

        return product.view_count.count()

    # 상품 디테일 조회
    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        payload = {}
        cached_product = cache.get(f'product_{pk}')
        try:
            product = self.get_object()
            if not cached_product:
                serializer = self.serializer_class(product)
                payload = serializer.data
                cache.set(f'product_{pk}', payload, 60 * 60)

            else:
                payload = cached_product
            payload.update({
                'view_count': self.update_view_count(product),
            })
            payload.update({
                'is_like': self.profile.wishes.filter(pk=pk).exists() if self.profile else False,
            })
            response = payload

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = payload

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    # 상품 작성된 리뷰 조회
    @action(detail=True, methods=['GET'], serializer_class=ReviewSerializer)
    def reviews(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            reviews = Review.objects.filter(id__in=Subquery(
                OrderProduct.objects.prefetch_related('review').filter(product_id=pk).annotate(
                    reviews=F('review')
                ).values_list('reviews', flat=True)
            ))
            serializer = self.serializer_class(reviews, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def contents(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        contents = Content.objects.all()
        serializer = ContentSerializer(contents, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def categories(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        categories = MainCategory.objects.all()
        serializer = MainCategorySerializer(categories, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(
        detail=False, methods=['POST'], serializer_class=CustomProductSerializer,
        queryset=CustomProduct.objects.all()
    )
    def customs(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, login_required=True)
            Basket.add(self.profile, serializer.instance)
            response = serializer.data

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @customs.mapping.get
    def custom_list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        serializer = self.serializer_class(self.get_queryset(), many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

from datetime import date

from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Product, ProductViewCount
from products.serializers import ProductSerializer


class BranduProductViewSet(BranduBaseViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    login_required = False

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

        finally:
            return product.view_count.count()

    # 상품 디테일 조회
    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            product = self.get_object()
            serializer = self.serializer_class(product)
            response = serializer.data
            response.update({
                'view_count': self.update_view_count(product)
            })
        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

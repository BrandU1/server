from django.db.models import Count, Subquery
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Content, Product
from products.serializers import ContentSerializer, ProductSimpleSerializer


class BranduContentBaseViewSet(BranduBaseViewSet):
    model = Content
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]
    login_required = False

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return ProductSimpleSerializer

    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        contents = self.get_queryset()
        serializer = self.get_serializer_class()(contents, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], url_path='hot-deal')
    def hot_deal(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        response = {}

        try:
            Product.objects.all()
            products = Product.objects.filter(id__in=Subquery(
                Product.objects.prefetch_related('view_count').values('id').annotate(
                    counts=Count('view_count'),
                ).order_by('-counts', '-id')[:10].values_list('id', flat=True)
            ))
            serializer = self.get_serializer_class()(products, many=True, context={'request': request})
            response = serializer.data

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            is_success = False
            response = {
                'code': 500,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)
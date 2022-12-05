from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import Product
from products.serializers import ProductSimpleSerializer
from search.models import Search
from search.serializers import SearchSerializer


class BranduSearchViewSet(BranduBaseViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = [AllowAny]
    login_required = True

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSimpleSerializer
        return self.serializer_class

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'history' or self.action == 'delete_all_history':
            permission_classes = [IsAuthenticated]
        elif self.action == 'delete_history':
            permission_classes = [IsAuthor]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('query', openapi.IN_QUERY, description='검색어', required=True,
                                             type=openapi.TYPE_STRING),
                           openapi.Parameter('filter', openapi.IN_QUERY, description='조회 필터링', required=False,
                                             type=openapi.TYPE_STRING)])
    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        query = self.request.query_params.get('query', None)

        try:
            Search.search_keyword(query, self.profile)
            products = Product.objects.prefetch_related('tags').filter(
                Q(name__icontains=query) | Q(tags__name__icontains=query)
            ).distinct().order_by('id')
            serializer = self.create_pagination(products, self.get_serializer_class())
            response = serializer.data

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': e.default_detail
            }

        except NotFound as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': e.default_detail
            }

        return brandu_standard_response(status_code=status_code, is_success=is_success, response=response)

    @action(detail=False, methods=['GET'])
    def history(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            searches = Search.objects.filter(profile=self.profile).values(
                'search_word', 'id'
            ).order_by('-id').values('search_word').order_by('search_word').distinct()
            serializer = self.get_serializer(searches, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': e.default_detail
            }
        return brandu_standard_response(status_code=status_code, is_success=is_success, response=response)

    @action(detail=False, methods=['DELETE'], url_path='history/(?P<pk>[0-9]+)')
    def delete_history(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            search = self.get_object()
            self.perform_destroy(search)
            response = {
                'message': '검색 기록이 삭제 되었습니다.'
            }

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': e.default_detail
            }

        return brandu_standard_response(status_code=status_code, is_success=is_success, response=response)

    @action(detail=False, methods=['DELETE'], url_path='history/all')
    def delete_all_history(self, request, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            queryset = self.get_queryset()
            self.perform_destroy(queryset)
            response = {
                'message': '검색 기록이 모두 삭제 되었습니다.'
            }

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': e.default_detail
            }

        return brandu_standard_response(status_code=status_code, is_success=is_success, response=response)

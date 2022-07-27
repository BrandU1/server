from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from datetime import date

from core.paginations import SmallResultsSetPagination
from products.models import Product
from products.serializers import ProductSerializer
from search.models import Search
from search.serializers import SearchSerializer, SearchRankSerializer


class SearchListAPIView(ListAPIView):
    """
    검색 쿼리 조회 API
    ---
    query: 검색어
    """
    query_param = openapi.Parameter('query', openapi.IN_QUERY, description='검색어', required=True,
                                    type=openapi.TYPE_STRING)
    filter_param = openapi.Parameter('filter', openapi.IN_QUERY, description='조회 필터링', required=False,
                                     type=openapi.TYPE_STRING)
    pagination_class = SmallResultsSetPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query is None:
            raise Exception('')

        if self.request.user:
            Search.objects.create(profile=self.request.user.profile, search_word=query)

        return self.queryset.filter(name__icontains=query).order_by('id')

    @swagger_auto_schema(manual_parameters=[query_param, filter_param])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SearchWordListAPIView(ListAPIView):
    """
    사용자 최근 검색어 조회 API
    ---
    로그인 인증 필요, 로그인이 되어있지 않다면 Exception
    """
    queryset = Search.objects.all()
    serializer_class = SearchSerializer

    def get_queryset(self):
        if not self.request.user:
            raise Exception('')
        return self.queryset.filter(profile=self.request.user.profile).order_by('-created')


class SearchWordRankListAPIView(ListAPIView):
    """
    브랜뉴 검색어 랭킹 조회 API
    ---
    로그인 인증 필요 없음. count 및 word 리턴
    """
    queryset = Search.objects.all()
    serializer_class = SearchRankSerializer

    def get_queryset(self):
        print(self.queryset.filter(created__gte=date.today()).values('search_word').annotate(
            count=Count('search_word')).order_by('count'))
        return self.queryset.filter(created__gte=date.today()).values('search_word').annotate(
            count=Count('search_word')).order_by('count')

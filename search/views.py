import operator

from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from core.paginations import SmallResultsSetPagination
from core.permissions import IsAuthor
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

        if self.request.user and self.request.user.is_authenticated:
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
    permission_classes = [IsAuthenticated]
    queryset = Search.not_deleted.all()
    serializer_class = SearchSerializer

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile).order_by('-created')[:10]


class SearchWordDeleteAPIView(APIView):
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        search = Search.objects.get(pk=pk)
        self.check_object_permissions(self.request, search)
        return search

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        search = self.get_object(pk)
        search.is_deleted = True
        search.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchWordDeleteAllAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        search = Search.objects.filter(profile=profile)
        search.update(is_delete=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchWordRankListAPIView(ListAPIView):
    """
    브랜뉴 검색어 랭킹 조회 API
    ---
    로그인 인증 필요 없음. count 및 word 리턴
    """
    queryset = Search.objects.all()
    serializer_class = SearchRankSerializer

    def get_queryset(self):
        return self.queryset.values('search_word').annotate(
            count=Count('search_word')).order_by('-count')[:10]

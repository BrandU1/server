from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import ReviewListSerializer
from core.paginations import SmallResultsSetPagination
from .models import Product, MainCategory, Review, SubCategory
from .serializers import ProductSimpleSerializer, MainCategorySerializer, ProductSerializer, ReviewSerializer


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class BranduHotDealListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class CategoryListView(ListAPIView):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


class ProductsByCategoryAPIView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        categories = SubCategory.objects.filter(main_category_id=pk)
        results = list()
        results.append({
            'id': 0,
            'category': '전체',
            'products': ProductSimpleSerializer(Product.objects.filter(category__main_category_id=pk), many=True).data,
        })
        for category in categories:
            products = Product.objects.filter(category=category)
            serializer = ProductSimpleSerializer(products, many=True)
            results.append({
                'id': category.id,
                'category': category.name,
                'products': serializer.data,
            })
        return Response(results, status=status.HTTP_200_OK)


class ProductCategoryListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        queryset = self.queryset.filter(category_id=pk)
        return queryset


class ProductReviewListAPIView(ListAPIView):
    pagination_class = SmallResultsSetPagination
    queryset = Review.not_deleted.all()
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()

        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        return self.queryset.filter(product=pk, is_write=True).order_by('created')


class ReviewCreateAPIView(CreateAPIView):  # 리뷰 생성 관련 Views
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

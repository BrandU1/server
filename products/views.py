from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.paginations import SmallResultsSetPagination
from .models import Product, MainCategory, Review
from .serializers import ProductSimpleSerializer, MainCategorySerializer, ReviewListSerializer, ProductSerializer, \
    ReviewSerializer


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BranduHotDealListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer


class CategoryListView(ListAPIView):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


class ProductCategoryListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        return self.queryset.filter(category_id=pk)


class ProductReviewListAPIView(ListAPIView):
    pagination_class = SmallResultsSetPagination
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()

        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        return self.queryset.filter(product=pk).order_by('created')


class ReviewCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

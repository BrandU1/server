from rest_framework.generics import ListAPIView, RetrieveAPIView

from core.paginations import SmallResultsSetPagination
from .models import Product, MainCategory, Review
from .serializers import ProductSimpleSerializer, MainCategorySerializer, ReviewListSerializer, ProductSerializer


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BranduHotDealListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer


class CategoryListView(ListAPIView):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


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

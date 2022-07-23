from rest_framework.generics import ListAPIView

from .models import Product, MainCategory
from .serializers import ProductSerializer, MainCategorySerializer


class BranduHotDealListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(ListAPIView):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

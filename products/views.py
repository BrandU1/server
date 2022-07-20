from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import ProductSerializer


class BranduHotDealListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

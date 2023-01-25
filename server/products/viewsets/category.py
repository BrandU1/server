from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from products.models import MainCategory, SubCategory
from products.serializers import MainCategorySerializer, SubCategorySerializer


class BranduCategoryViewSet(BranduBaseViewSet):
    model = MainCategory
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer
    permission_classes = [AllowAny]
    login_required = False

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return SubCategorySerializer
    #
    #     return self.serializer_class

    # 전체 카테고리 목록 조회

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            category = SubCategory.objects.filter(main_category_id=pk).values('id', 'name', 'backdrop_image')
            serializer = self.get_serializer_class()(category, many=True)
            response = {
                'main_category': pk,
                'sub_categories': serializer.data
            }

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

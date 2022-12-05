from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from events.models import CouponHold
from events.serializers import CouponHoldSerializer


class BranduCouponViewSet(BranduBaseViewSet):
    model = CouponHold
    serializer_class = CouponHoldSerializer
    queryset = CouponHold.objects.all()
    permission_classes = [IsAuthenticated]
    login_required = True

    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        coupons = self.get_queryset()
        serializer = self.serializer_class(coupons, many=True)
        response = serializer.data
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

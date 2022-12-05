from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from events.models import Advertisement
from events.serializers import AdvertisementSerializer


class BranduEventViewSet(BranduBaseViewSet):
    model = Advertisement
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]
    login_required = False

    @action(detail=False, methods=['GET'])
    def carousel(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        carousels = self.get_queryset().filter(type='CAROUSEL')
        serializer = self.get_serializer(carousels, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def banner(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        banners = self.get_queryset().filter(type='BANNER')
        serializer = self.get_serializer(banners, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from core.response import brandu_standard_response
from core.views import BranduBaseViewSet
from services.models import FAQ, MainInfo, Inquiry, Notice
from services.serializers import FAQSerializer, MainInfoSerializer, InquirySerializer, NoticeSerializer


class BranduServiceViewSet(BranduBaseViewSet):
    model = FAQ
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    login_required = False

    def get_queryset(self) -> QuerySet:
        if self.action == 'notices':
            self.queryset = Notice.objects.all()
        elif self.action == 'main-infos':
            self.queryset = MainInfo.objects.all()
        return super(BranduServiceViewSet, self).get_queryset()

    def get_serializer_class(self):
        if self.action == 'notices' or self.action == 'notices_detail':
            return NoticeSerializer
        elif self.action == 'main_infos' or self.action == 'main_infos_detail':
            return MainInfoSerializer
        return self.serializer_class

    @action(detail=False, methods=['GET'])
    def all(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        response = {}

        try:
            faqs = FAQ.objects.order_by('created')[:10]
            main_infos = MainInfo.objects.order_by('created')[:10]
            response = {
                'faqs': FAQSerializer(faqs, many=True).data,
                'main_infos': MainInfoSerializer(main_infos, many=True).data
            }

            if self.profile:
                inquires = Inquiry.objects.filter(profile=self.profile).order_by('created')[:10]
                response.update({
                    'inquires': InquirySerializer(inquires, many=True).data
                })

        except PermissionDenied as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.default_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def notices(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        notices = self.get_queryset()
        serializer = self.get_serializer(notices, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], url_path='notices/(?P<pk>[0-9]+)')
    def notices_detail(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        notice = get_object_or_404(Notice, pk=pk)
        serializer = self.get_serializer(notice)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def main_infos(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        main_infos = self.get_queryset()
        serializer = self.get_serializer(main_infos, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], url_path='main_infos/(?P<pk>[0-9]+)')
    def main_infos_detail(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        main_info = get_object_or_404(MainInfo, pk=pk)
        serializer = self.get_serializer(main_info)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def faqs(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        faqs = self.get_queryset()
        serializer = self.get_serializer(faqs, many=True)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], url_path='faqs/(?P<pk>[0-9]+)')
    def faqs_detail(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        faq = get_object_or_404(FAQ, pk=pk)
        serializer = self.get_serializer(faq)
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

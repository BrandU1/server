from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from core.paginations import XSmallResultsSetPagination
from core.permissions import IsAuthor
from services.models import Notice, Inquiry, FAQ, MainInfo
from services.serializers import NoticeSerializer, InquirySerializer, FAQSerializer, MainInfoSerializer


class NoticeListAPIView(ListAPIView):
    queryset = Notice.objects.all().order_by('created')
    serializer_class = NoticeSerializer


class ServicesListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        faq = FAQ.objects.all().order_by('created')[:4]
        faq_serializer = FAQSerializer(faq, many=True)
        main_info = MainInfo.objects.all().order_by('created')[:4]
        main_info_serializer = MainInfoSerializer(main_info, many=True)

        if self.request.user and not self.request.user.is_anonymous:
            profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
            inquiry = Inquiry.objects.filter(profile=profile).order_by('created')[:4]
            inquiry_serializer = InquirySerializer(inquiry, many=True)
            return Response({
                'main_infos': main_info_serializer.data,
                'faqs': faq_serializer.data,
                'inquiries': inquiry_serializer.data,
            }, status=status.HTTP_200_OK)

        return Response({
            'main_infos': main_info_serializer.data,
            'faqs': faq_serializer.data,
        }, status=status.HTTP_200_OK)


class MainInfoListAPIVIew(ListAPIView):
    queryset = MainInfo.objects.all()
    serializer_class = MainInfoSerializer
    pagination_class = XSmallResultsSetPagination


class FAQListAPIView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = XSmallResultsSetPagination


class InquiryListCreateAPIView(ListCreateAPIView):
    queryset = Inquiry.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer
    pagination_class = XSmallResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        return self.queryset.filter(profile=profile).order_by('created')


class InquiryUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Inquiry.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = InquirySerializer

    def get_queryset(self):
        inquiry = self.queryset.get(pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, inquiry)
        return super(InquiryUpdateAPIView, self).get_queryset()

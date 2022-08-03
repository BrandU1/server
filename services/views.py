from django.shortcuts import render
from rest_framework.generics import ListAPIView

from services.models import Notice
from services.serializers import NoticeSerializer


class NoticeListAPIView(ListAPIView):
    queryset = Notice.objects.all().order_by('created')
    serializer_class = NoticeSerializer


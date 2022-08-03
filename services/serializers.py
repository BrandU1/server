from rest_framework import serializers

from services.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'created', 'title', 'description']

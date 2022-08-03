from rest_framework import serializers

from accounts.models import Profile
from services.models import Notice, Inquiry


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'created', 'title', 'description']


class InquirySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    is_answer = serializers.BooleanField(read_only=True)

    class Meta:
        model = Inquiry
        fields = ['id', 'created', 'title', 'description', 'is_answer']

    def create(self, validated_data):
        user = self.context.get("request").user
        profile = Profile.get_profile_or_exception(user.profile.id)
        return Inquiry.objects.create(profile=profile, **validated_data)

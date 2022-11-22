from django.core.files.base import ContentFile
from rest_framework import serializers

from accounts.models import Profile
from services.models import Notice, Inquiry, FAQ, MainInfo, InquiryImage


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'created', 'title', 'description']


class MainInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainInfo
        fields = ['id', 'title', 'description', 'created']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'title', 'description', 'created']


class InquiryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = InquiryImage
        fields = ['id', 'image']


class InquirySerializer(serializers.ModelSerializer):
    images = InquiryImageSerializer(many=True, source='inquiryimage_set', required=False)

    class Meta:
        model = Inquiry
        fields = ['id', 'title', 'description', 'images', 'created', 'is_answer']

    def create(self, validated_data):
        request = self.context.get("request", None)
        images = request.data.getlist('images')
        profile = Profile.get_profile_or_exception(request.user.profile.id)
        inquiry = Inquiry.objects.create(profile=profile, **validated_data)
        for idx, image in enumerate(images):
            inquiry_image = InquiryImage(inquiry=inquiry)
            inquiry_image.image.save(f'{inquiry.id}-{idx}.png', image)
        return inquiry

    def update(self, instance: Inquiry, validated_data):
        request = self.context.get("request", None)
        images = request.data.getlist('images')
        instance.objects.update(**validated_data)
        instance.inquiryimage_set.all().delete()
        for image in images:
            serializer = InquiryImageSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save()
        return instance

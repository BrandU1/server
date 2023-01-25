from rest_framework import serializers

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
    images = InquiryImageSerializer(many=True, required=False)

    class Meta:
        model = Inquiry
        fields = ['id', 'title', 'description', 'images', 'created', 'is_answer']
        extra_kwargs = {
            'is_answer': {'read_only': True},
        }

    def create(self, validated_data):
        images = validated_data.pop('images', None)
        inquiry = Inquiry.objects.create(**validated_data)
        if not images:
            return inquiry
        inquiry.images.set(map(lambda image: InquiryImage.objects.create(inquiry=inquiry, image=image), images))
        return inquiry

    def update(self, instance: Inquiry, validated_data):
        images = validated_data.pop('images', None)
        instance.save({
            validated_data
        })
        if not images:
            return instance
        instance.images.set(map(lambda image: InquiryImage.objects.create(inquiry=instance, image=image), images))
        return instance

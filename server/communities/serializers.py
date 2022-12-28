from rest_framework import serializers

from communities.models import Post, PostImage


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'backdrop_image', 'profile', 'created']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'profile', 'title', 'backdrop_image', 'content', 'images']
        read_only_fields = ['profile', 'images']
        extra_kwargs = {
            'backdrop_image': {'required': False},
            'content': {'required': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['images'] = [
            self.context['request'].build_absolute_uri(image.image.url)
            for image in instance.images.all()
        ]
        return ret


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'post']
        read_only_fields = ['post']

    def create(self, validated_data):
        return super().create(validated_data)

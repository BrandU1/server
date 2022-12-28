from rest_framework import serializers

from communities.models import Post, PostImage


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'backdrop_image', 'profile', 'created']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'profile', 'title', 'backdrop_image', 'content']
        read_only_fields = ['profile']
        extra_kwargs = {
            'backdrop_image': {'required': False},
        }


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']

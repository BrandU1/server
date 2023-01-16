from rest_framework import serializers

from accounts.serializers import ProfileSimpleSerializer
from communities.models import Post, PostImage, Comment


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'backdrop_image', 'profile', 'created']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'profile', 'title', 'backdrop_image', 'content', 'created']
        read_only_fields = ['profile']
        extra_kwargs = {
            'backdrop_image': {'required': False},
        }


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'profile', 'comment', 'created']
        read_only_fields = ['profile']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile'] = ProfileSimpleSerializer(instance.profile).data
        return data

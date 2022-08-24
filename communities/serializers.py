from rest_framework import serializers

from accounts.serializers import ProfileSimpleSerializer
from communities.models import Post, Content, Comment


class ContentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Content
        fields = ['priority', 'image', 'description']


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'profile', 'comment']


class PostSimpleSerializer(serializers.ModelSerializer):
    profile = ProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'backdrop_image', 'profile', 'created']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    profile = ProfileSimpleSerializer(read_only=True)
    contents = ContentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'title', 'backdrop_image', 'comments', 'contents']

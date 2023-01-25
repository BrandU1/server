from rest_framework import serializers

from accounts.models import Profile
from accounts.serializers import ProfileSimpleSerializer
from communities.models import Post, PostImage, Comment


class PostSimpleSerializer(serializers.ModelSerializer):
    is_scrap = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'backdrop_image', 'profile', 'created', 'is_scrap']

    def get_is_scrap(self, obj) -> bool:
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        profile = Profile.get_profile_or_exception(request.user.profile.id)
        return profile.scraps.filter(id=obj.pk).exists()


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

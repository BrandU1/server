from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers import ProfileDetailSerializer


class ProfileDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.user:
            profile = Profile.objects.get(user=self.request.user.id)
            serializer = ProfileDetailSerializer(profile)
            return Response(serializer.data)
        raise Exception('')


class ProfileFollowAPIView(APIView):
    """
    사용자 팔로우 · 언팔로우 API
    ---
    
    """
    def post(self, request, *args, **kwargs):
        if self.request.user:
            profile_id = self.request.data['user']
            profile = Profile.objects.get(user=self.request.user.id)
            profile.follow(Profile.get_profile_or_exception(profile_id))
        raise Exception('')

    def delete(self, request, *args, **kwargs):
        if self.request.user:
            profile_id = self.request.data['user']
            profile = Profile.objects.get(user=self.request.user.id)
            profile.unfollow(Profile.get_profile_or_exception(profile_id))
        raise Exception('')

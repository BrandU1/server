from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from accounts.models import Profile
from accounts.serializers import ProfileSummarySerializer, ProfileEditSerializer


class ProfileDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        serializer = ProfileSummarySerializer(profile)
        return Response(serializer.data)


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


class ProfileEditAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileEditSerializer

    def get_object(self):
        return Profile.get_profile_or_exception(self.request.user.profile.id)

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from accounts.models import Profile
from accounts.serializers import ProfileSummarySerializer, ProfileEditSerializer, AddressEditSerializer


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        serializer = ProfileSummarySerializer(profile)
        return Response(serializer.data)


class ProfileFollowAPIView(APIView):
    """
    사용자 팔로우 · 언팔로우 API
    ---
    """
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileEditSerializer

    def get_object(self):
        return Profile.get_profile_or_exception(self.request.user.profile.id)


class AddressEditAPIView(APIView):
    """
    사용자 주소 관련 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        addresses = profile.address_set.all()
        serializer = AddressEditSerializer(addresses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AddressEditSerializer)
    def post(self, request, *args, **kwargs):
        serializer = AddressEditSerializer(data=self.request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AddressEditSerializer)
    def put(self, request, *args, **kwargs):
        serializer = AddressEditSerializer(data=self.request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

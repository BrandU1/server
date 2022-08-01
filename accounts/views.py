from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView

from accounts.models import Profile, Address
from accounts.serializers import ProfileSummarySerializer, ProfileEditSerializer, AddressSerializer, ProfileSerializer
from core.permissions import IsAuthor
from products.models import Review
from products.serializers import ReviewListSerializer, ReviewSerializer


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class AddressListAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile.id)


class AddressEditAPIView(APIView):
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        address = Address.objects.get(pk=pk)
        self.check_object_permissions(self.request, address)
        return address

    @swagger_auto_schema(request_body=AddressSerializer)
    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=self.request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_200_OK)


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewSerializer
        return ReviewListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile.id)


class ReviewAPIView(APIView):
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        review = Review.objects.get(pk=pk)
        self.check_object_permissions(self.request, review)
        return review

    @swagger_auto_schema(request_body=ReviewSerializer)
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=self.request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        review = self.get_object(pk)
        review.is_deleted = True
        review.save()
        return Response(status=status.HTTP_200_OK)

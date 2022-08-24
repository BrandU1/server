from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView, \
    get_object_or_404

from accounts.models import Profile, Address, Notify, Bucket
from accounts.serializers import ProfileSummarySerializer, AddressSerializer, ProfileSerializer, ProfilePointSerializer, \
    NotifySerializer, BucketSerializer
from communities.models import Post
from communities.serializers import PostSimpleSerializer
from core.permissions import IsAuthor
from products.models import Review
from products.serializers import ReviewListSerializer, ReviewSerializer


class ProfileAPIView(APIView):
    """
    사용자 프로필 정보 조회 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailAPIView(APIView):
    """
    사용자 특수 정보(쿠폰, 포인트 등등...) 요약 조회 API
    ---
    """
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
        profile_id = self.request.data['user']
        profile = Profile.objects.get(user=self.request.user.id)
        profile.follow(Profile.get_profile_or_exception(profile_id))
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        profile_id = self.request.data['user']
        profile = Profile.objects.get(user=self.request.user.id)
        profile.unfollow(Profile.get_profile_or_exception(profile_id))
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileEditAPIView(UpdateAPIView):
    """
    사용자 프로필 정보 수정 API
    ---
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.get_profile_or_exception(self.request.user.profile.id)


class ProfilePointAPIView(APIView):
    """
    사용자 포인트 조회 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        serializer = ProfilePointSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressListAPIView(ListCreateAPIView):
    """
    사용자 배송지 정보 관련 조회 및 생성 API
    ---
    """
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile.id).order_by('-is_main', 'created')


class AddressEditAPIView(APIView):
    """
    사용자 배송지 수정 및 삭제 API
    ---
    """
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        address = Address.objects.get(pk=pk)
        self.check_object_permissions(self.request, address)
        return address

    @swagger_auto_schema(request_body=AddressSerializer)
    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=self.request.data, context={'request': request}, partial=True)
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


class SetMainAddressAPIView(APIView):
    """
    기본 배송지 설정 API
    """
    def patch(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        pk = kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        address = Address.objects.get(pk=pk)

        if address.profile != profile:
            raise Exception('')

        address.set_main()
        return Response(status=status.HTTP_201_CREATED)


class ReviewAPIView(APIView):
    """
    사용자 리뷰 수정 및 삭제 API
    ---
    """
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


class NotifyAPIView(APIView):
    """
    사용자 1:1 문의 조회 및 수정 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        notify = Notify.objects.get(profile=profile)
        serializer = NotifySerializer(notify)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        notify = Notify.objects.get(profile=profile)
        serializer = NotifySerializer(notify, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListAPIView(ListAPIView):
    """
    사용자 작성 리뷰 리스트 조회 API
    ---
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile).order_by('created')


class FavoriteCreateAPIView(APIView):
    """
    사용자 관심 상품 추가 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        bucket = Bucket.objects.create(profile=profile, product_id=pk, amount=1)
        serializer = BucketSerializer(bucket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavoriteListAPIView(ListAPIView):
    """
    관심 상품 리스트 조회 API
    ---
    """
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile, is_purchase=False)


class BucketListAPIView(ListAPIView):
    """
    장바구니 리스트 조회 API
    ---
    """
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile, is_purchase=True)


class BucketChangeDeleteAPIView(APIView):
    """
    관심 상품 -> 장바구니 조회 및 장바구니 삭제 API
    ---
    """
    permission_classes = [IsAuthor]

    def get_object(self, pk):
        bucket = Bucket.objects.get(pk=pk)
        self.check_object_permissions(self.request, bucket)
        return bucket

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        bucket = self.get_object(pk)
        if bucket.is_purchase:
            raise Exception('')
        bucket.is_purchase = True
        bucket.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        bucket = self.get_object(pk)
        bucket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostScrappedListAPIView(ListAPIView):
    """
    사용자 스크랩 게시글 조회 API
    ---
    """
    serializer_class = PostSimpleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return profile.scrapped.all()


class PostScrappedCreateAPIView(APIView):
    """
    사용자 스크랩 생성(스크랩 하기) 및 삭제 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        post = get_object_or_404(Post, pk=pk)
        profile.scrapped.add(post)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise Exception('')
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        post = get_object_or_404(Post, pk=pk)
        profile.scrapped.remove(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

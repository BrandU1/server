from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, get_object_or_404

from accounts.models import Profile, Address, Notify, Basket, WishList, Following
from accounts.serializers import AddressSerializer, ProfileSerializer, ProfilePointSerializer, \
    NotifySerializer, BasketSerializer, WishListSerializer, ProfileSimpleSerializer, FollowingProfileSerializer
from communities.models import Post
from communities.serializers import PostSimpleSerializer
from core.exceptions.common import KeyDoesNotExistException, ProfileNotMatchException
from core.exceptions.product import RelationAlreadyExistException, RelationDoesNotExistException
from core.permissions import IsAuthor
from orders.models import Order
from orders.serializers import OrderSerializer
from products.models import Review, Product
from products.serializers import ReviewSerializer


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


class ProfileFollowAPIView(APIView):
    """
    사용자 팔로우 · 언팔로우 API
    ---
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'profile_id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def post(self, request, *args, **kwargs):
        profile_id = self.request.data['profile_id']
        profile = Profile.objects.get(user=self.request.user.id)
        profile.follow(Profile.get_profile_or_exception(profile_id))
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'profile_id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def delete(self, request, *args, **kwargs):
        profile_id = self.request.data['profile_id']
        profile = Profile.objects.get(user=self.request.user.id)
        profile.unfollow(Profile.get_profile_or_exception(profile_id))
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileFollowListAPIView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        profile = Profile.get_profile_or_exception(pk)
        follower_serializer = FollowingProfileSerializer(profile.following.all(), many=True)
        following_serializer = FollowingProfileSerializer(profile.following.all(), many=True)
        return Response({
            'follower': follower_serializer.data,
            'following': following_serializer.data,
        }, status=status.HTTP_200_OK)


class ProfileEditAPIView(UpdateAPIView):
    """
    사용자 프로필 정보 수정 API
    ---
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    @swagger_auto_schema(request_body=ProfileSerializer)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self) -> Profile:
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


class ProfileSummaryAPIView(APIView):
    """
    사용자 요약 정보 (포인트, 찜한 상품 갯수 등등...)
    ---
    """
    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        orders = profile.order_set
        return Response({
            'my': {
                'wish': profile.wish.count(),
                'basket': profile.basket.count(),
                'scrap': profile.scrapped.count(),
                'coupon': profile.couponhold_set.count(),
                'point': profile.point,
            },
            'orders': {
                'all': orders.all().count(),
                'paid': len([order for order in orders.all() if order.status == 'paid']),
                'delivery': len([order for order in orders.all() if order.status == 'delivery']),
                'complete': len([order for order in orders.all() if order.status == 'complete']),
                'confirm': len([order for order in orders.all() if order.status == 'confirm'])
            }
        }, status=status.HTTP_200_OK)


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
    def patch(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=self.request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_200_OK)


class SetMainAddressAPIView(APIView):
    """
    기본 배송지 설정 API
    """
    def patch(self, request, pk=None, *args, **kwargs):
        profile = Profile.get_profile_or_exception(self.request.user.profile.id)
        if pk is None:
            raise KeyDoesNotExistException()
        address = Address.objects.get(pk=pk)

        if address.profile != profile:
            raise ProfileNotMatchException()

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

    def get(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ReviewSerializer)
    def put(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=self.request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        review = self.get_object(pk)
        review.is_deleted = True
        review.save()
        return Response(status=status.HTTP_200_OK)


class NotifyAPIView(APIView):
    """
    사용자 알림 설정 조회 및 수정 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        notify, _ = Notify.objects.get_or_create(profile=profile)
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


class WishListAPIView(APIView):
    """
    사용자 관심 상품 생성 및 삭제 관련 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        product = get_object_or_404(Product, pk=pk)
        if profile.wish.filter(id=product.id).exists():
            raise RelationAlreadyExistException()
        profile.wish.add(product)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        product = get_object_or_404(Product, pk=pk)
        if profile.wish.filter(id=product.id).exists():
            profile.wish.remove(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise RelationDoesNotExistException()


class WishListListAPIView(ListAPIView):
    """
    관심 상품 리스트 조회 API
    ---
    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class BasketAPIView(APIView):
    """
    장바구니 생성 및 삭제 관련 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        product = get_object_or_404(Product, pk=pk)
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        if profile.basket.filter(id=product.id).exists():
            raise RelationAlreadyExistException()
        profile.basket.add(product)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        product = Product.objects.get(pk=pk)
        if profile.basket.filter(id=product.id).exists():
            profile.basket.remove(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise RelationDoesNotExistException()


class BasketPurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BasketSerializer(many=True))
    def patch(self, request, *args, **kwargs):

        return Response(status=status.HTTP_200_OK)


class BasketListAPIView(ListAPIView):
    """
    장바구니 리스트 조회 API
    ---
    """
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile)


class BasketPurchaseUpdateAPIView(APIView):
    @swagger_auto_schema(request_body=BasketSerializer(many=True))
    def patch(self, request, *args, **kwargs):
        basket_ids = [instance['id'] for instance in self.request.data]
        for idx, basket_id in enumerate(basket_ids):
            basket = Basket.objects.get(pk=basket_id)
            basket.amount = self.request.data[idx]['amount']
            basket.is_purchase = self.request.data[idx]['is_purchase']
            basket.save()
        return Response(status=status.HTTP_200_OK)


class PurchaseListAPIView(ListAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile, is_purchase=True)


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

    def post(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        post = get_object_or_404(Post, pk=pk)
        profile.scrapped.add(post)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            raise KeyDoesNotExistException()
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        post = get_object_or_404(Post, pk=pk)
        profile.scrapped.remove(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        return self.queryset.filter(profile=profile)

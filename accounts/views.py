from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, Notify, Basket, WishList
from accounts.serializers import (
    ProfileSerializer, ProfilePointSerializer,
    NotifySerializer, BasketSerializer, WishListSerializer
)
from communities.models import Post
from communities.serializers import PostSimpleSerializer
from core.exceptions.common import KeyDoesNotExistException
from core.exceptions.product import RelationAlreadyExistException, RelationDoesNotExistException
from core.permissions import IsAuthor
from core.views import BranduBaseViewSet
from orders.models import Order
from orders.serializers import OrderSerializer
from products.models import Review, Product
from products.serializers import ReviewSerializer


class BranduProfileViewSet(BranduBaseViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_permissions(self) -> list:
        permission_classes = self.permission_classes
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [*permission_classes, IsAuthor]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['PATCH'])
    def edit(self, request, *args, **kwargs):
        try:
            profile = self.profile
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def me(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def point(self, request, *args, **kwargs):
        serializer = ProfilePointSerializer(self.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def summary(self, request, *args, **kwargs):
        self.profile.order_set.filter(status='paid').count()


class BranduReviewViewSet(BranduBaseViewSet):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        return super(BranduReviewViewSet, self).list(request, *args, **kwargs)

    def perform_destroy(self, instance: Review) -> None:
        instance.is_deleted = True
        instance.save()


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


class WishListAPIView(APIView):
    """
    사용자 관심 상품 생성 및 삭제 관련 API
    ---
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, *args, **kwargs):
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        product = get_object_or_404(Product, pk=pk)
        if profile.wish.filter(id=product.id).exists():
            raise RelationAlreadyExistException()
        profile.wish.add(product)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
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
        product_ids = [instance['product_id'] for instance in self.request.data]
        profile = Profile.get_profile_or_exception(profile_id=self.request.user.profile.id)
        for idx, product_id in enumerate(product_ids):
            basket = Basket.objects.get(product_id=product_id, profile=profile)
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

from django.db.models import Count, Subquery
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.models import Profile, Notify, Basket, WishList, Address
from accounts.serializers import ProfileSerializer, ProfilePointSerializer, NotifySerializer, \
    FollowingProfileSerializer, BasketSerializer, WishListSerializer, AddressSerializer
from communities.models import Post
from communities.serializers import PostSimpleSerializer
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


class BranduProfileViewSet(BranduBaseViewSet):
    model = Profile
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    login_required = True

    @staticmethod
    def get_profile(pk=None):
        return get_object_or_404(Profile, pk=pk)

    def get_permissions(self) -> list:
        permission_classes = self.permission_classes
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [*permission_classes, IsAuthor]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['PATCH'])
    def edit(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        try:
            serializer = self.get_serializer(self.profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except Profile.DoesNotExist as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        profile = self.get_profile(pk=pk)
        serializer = self.serializer_class(profile)
        response = serializer.data
        response.update({
            'followers': profile.followers.count(),
            'followings': profile.following.count()
        })
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'])
    def me(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        serializer = self.serializer_class(self.profile)
        response = serializer.data
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], serializer_class=ProfilePointSerializer)
    def point(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='summary/order')
    def summary_order(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        summaries = self.profile.orders.values('order_status').annotate(count=Count('order_status'))
        response = summaries

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], url_path='summary/profile')
    def summary_profile(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        summaries = Profile.objects.annotate(
            wish_count=Count('wishes'),
            basket_count=Count('baskets'),
            scrap_count=Count('scraps'),
            coupon_count=Count('coupons'),
        ).values(
            'wish_count', 'basket_count', 'scrap_count', 'coupon_count', 'point'
        ).get(pk=self.profile.pk)
        response = summaries

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], serializer_class=NotifySerializer)
    def notify(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        notify = None

        try:
            notify = self.profile.notify

        except Notify.DoesNotExist as e:
            notify = Notify.objects.create(profile=self.profile)

        finally:
            serializer = self.get_serializer(notify)
            response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @notify.mapping.patch
    def notify_update(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            notify = self.profile.notify
            serializer = self.get_serializer(notify, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['GET'], detail=False, serializer_class=FollowingProfileSerializer, url_path='follows')
    def follow_list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        profile: Profile = self.profile
        response = {
            'follower': self.serializer_class(profile.followers.all(), many=True).data,
            'following': self.serializer_class(profile.following.all(), many=True).data
        }
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['GET'], detail=False, queryset=Basket.objects.all(), serializer_class=BasketSerializer)
    def baskets(self, request, *args, **kwargs):
        """ 장바구니 목록 조회 API """
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            baskets = Basket.objects.filter(profile=self.profile)
            serializer = self.serializer_class(baskets, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['GET'], detail=False, queryset=WishList.objects.all(), serializer_class=WishListSerializer)
    def wishes(self, request, *args, **kwargs):
        """사용자 위시 리스트 목록 조회 API"""
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            wishes = WishList.objects.filter(profile=self.profile)
            serializer = self.serializer_class(wishes, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'error': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['GET'], detail=False, queryset=Address.not_deleted.all(), serializer_class=AddressSerializer)
    def addresses(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            addresses = Address.not_deleted.filter(profile=self.profile)
            serializer = self.serializer_class(addresses, many=True)
            response = serializer.data

        except PermissionDenied as e:
            status_code = status.HTTP_403_FORBIDDEN
            is_success = False
            response = {
                'code': 403,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @addresses.mapping.post
    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = serializer.data

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['GET'], detail=False)
    def scraps(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            posts = Post.objects.filter(
                id__in=Subquery(
                    self.profile.scraps.all().values('id')
                )
            )
            serializer = PostSimpleSerializer(posts, many=True)
            response = serializer.data

        except ValidationError as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(methods=['POST'], detail=False, url_path='scraps/(?P<pk>[0-9]+)')
    def create_scrap(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True
        response = {}

        if not self.profile.scraps.filter(id=pk).exists():
            post = get_object_or_404(Post, pk=pk)
            self.profile.scraps.add(post)
            response = {
                'message': '스크랩 되었습니다.'
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @create_scrap.mapping.delete
    def delete_scrap(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True
        response = {}

        if self.profile.scraps.filter(id=pk).exists():
            post = get_object_or_404(Post, pk=pk)
            self.profile.scraps.remove(post)
            response = {
                'message': '스크랩 삭제되었습니다..'
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

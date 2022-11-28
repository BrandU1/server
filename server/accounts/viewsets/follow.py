from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import Profile
from accounts.serializers import FollowingProfileSerializer
from core.exceptions.product import RelationDoesNotExistException, RelationAlreadyExistException
from core.exceptions.profile import ProfileNotAllowException
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


class BranduFollowViewSet(BranduBaseViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingProfileSerializer
    login_required = True

    @staticmethod
    def get_profile(pk=None):
        return get_object_or_404(Profile, pk=pk)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            profile = self.get_profile(pk=pk)
            response = {
                'follower': self.serializer_class(profile.followers.all(), many=True).data,
                'following': self.serializer_class(profile.following.all(), many=True).data
            }

        except Profile.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            is_success = False
            response = {
                'code': 404,
                'message': 'Profile does not exist'
            }
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        profile: Profile = self.profile
        response = {
            'follower': self.serializer_class(profile.followers.all(), many=True).data,
            'following': self.serializer_class(profile.following.all(), many=True).data
        }
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=True, methods=['POST'], description='팔로우 추가')
    def follow(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True
        profile = self.get_profile(pk=pk)

        try:
            self.profile.follow(profile=profile)
            response = {
                'message': '팔로우 되었습니다.'
            }

        except ProfileNotAllowException as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'message': str(e.detail)
            }

        except RelationAlreadyExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @follow.mapping.delete
    def unfollow(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True
        profile = self.get_profile(pk=pk)

        try:
            self.profile.unfollow(profile=profile)
            response = {
                'message': '팔로우가 해제되었습니다.'
            }

        except ProfileNotAllowException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        except RelationDoesNotExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

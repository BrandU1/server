from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from accounts.serializers import FollowingProfileSerializer
from core.exceptions.product import RelationDoesNotExistException
from core.exceptions.profile import ProfileNotAllowException
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


class BranduFollowViewSet(BranduBaseViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingProfileSerializer

    def list(self, request, *args, **kwargs):
        status_code = status.HTTP_400_BAD_REQUEST
        is_success = True
        profile: Profile = self.profile
        response = {
            'follower': FollowingProfileSerializer(profile.followers.all(), many=True).data,
            'following': FollowingProfileSerializer(profile.following.all(), many=True).data
        }
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=True, methods=['POST'], description='팔로우 추가')
    def follow(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        who = get_object_or_404(Profile, pk=pk)

        try:
            self.profile.follow(profile=who)
            response = {
                'message': '팔로우 되었습니다.'
            }

        except ProfileNotAllowException as e:
            status_code = status.HTTP_400_BAD_REQUEST
            is_success = False
            response = {
                'code': 400,
                'error': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @follow.mapping.delete
    def unfollow(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True
        who = get_object_or_404(Profile, pk=pk)

        try:
            self.profile.unfollow(profile=who)
            response = {
                'message': '팔로우가 해제되었습니다.'
            }

        except ProfileNotAllowException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'error': str(e.default_detail)
            }

        except RelationDoesNotExistException as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'error': str(e.default_detail)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

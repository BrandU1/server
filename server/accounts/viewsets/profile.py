from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.models import Profile
from accounts.serializers import ProfileSerializer, ProfilePointSerializer, NotifySerializer
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


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
            serializer = self.get_serializer(self.profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

    @action(detail=False, methods=['GET'])
    def summary(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        self.profile.orders.filter(status='paid').count()
        response = {}
        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['GET'], serializer_class=NotifySerializer)
    def notify(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        notify = self.profile.notify
        serializer = self.get_serializer(notify)

        response = {
            'notify': serializer.data
        }

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

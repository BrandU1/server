from django.db.models import QuerySet, Model
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

from accounts.models import Profile


class BranduBaseViewSet(GenericViewSet):
    model = Model
    login_required = False

    def get_authenticate_profile(self) -> Profile:
        if not self.request.user.is_authenticated:
            raise PermissionDenied('로그인하고 다시 시도해주세요.')
        if self.request.user.is_anonymous:
            raise Profile.DoesNotExist('프로필이 존재하지 않는 회원입니다.')
        return Profile.get_profile_or_exception(self.request.user.profile.id)

    @property
    def profile(self) -> Profile:
        return self.get_authenticate_profile()

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        if getattr(self, 'swagger_fake_view', False):
            queryset = QuerySet()
            return queryset.none()

        if hasattr(self.model, 'not_deleted'):
            queryset = self.model.not_deleted.all()

        if self.login_required:
            try:
                queryset = queryset.filter(profile=self.profile)

            except PermissionDenied:
                return queryset.none()

        return queryset

    def perform_create(self, serializer, *args, **kwargs) -> None:
        if self.login_required:
            serializer.save(profile=self.profile, **kwargs)
        serializer.save(**kwargs)

    def perform_destroy(self, instance) -> None:
        if hasattr(instance, 'is_deleted'):
            instance.is_deleted = True
            instance.save()
        else:
            instance.delete()

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        if self.login_required:
            context.update({'profile': self.profile})
        return context

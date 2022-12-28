from django.core.cache import cache
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated

from communities.models import Post
from communities.serializers import PostSerializer, PostImageSerializer
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


class BranduPostViewSet(BranduBaseViewSet):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    login_required = False

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['partial_update', 'destroy', 'images']:
            permission_classes = [IsAuthor]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['GET'])
    def best(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True
        cached = cache.get('best_post')

        if not cached:
            posts = Post.objects.prefetch_related('likes').annotate(
                likes_count=Count('likes')
            ).values('id', 'title', 'likes_count', 'backdrop_image')[:10]
            cache.set('best_post', posts, 60 * 60)
            payload = posts
        else:
            payload = cached

        return brandu_standard_response(is_success=is_success, response=payload, status_code=status_code)

    def create(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, login_required=True)
            response = serializer.data

        except ValidationError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            is_success = False
            response = {
                'code': 500,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def retrieve(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        post = self.get_object()
        serializer = self.serializer_class(post, context={'request': request})
        response = serializer.data

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    def partial_update(self, request, pk, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            post = self.get_object()
            serializer = self.serializer_class(post, data=request.data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = serializer.data

        except ValidationError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            is_success = False
            response = {
                'code': 500,
                'message': str(e)
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

    @action(detail=False, methods=['POST'], serializer_class=PostImageSerializer)
    def images(self, request, *args, **kwargs):
        status_code = status.HTTP_201_CREATED
        is_success = True

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            image = serializer.data['image']
            response = {
                'image': request.build_absolute_uri(image)
            }

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

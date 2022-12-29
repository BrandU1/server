from rest_framework import status
from rest_framework.exceptions import ValidationError

from communities.models import Comment
from communities.serializers import PostCommentSerializer
from core.permissions import IsAuthor
from core.response import brandu_standard_response
from core.views import BranduBaseViewSet


class BranduCommentViewSet(BranduBaseViewSet):
    model = Comment
    serializer_class = PostCommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthor]
    login_required = False

    def partial_update(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_200_OK
        is_success = True

        try:
            comment = self.get_object()
            serializer = PostCommentSerializer(comment, data=request.data)
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

    def destroy(self, request, pk=None, *args, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        is_success = True

        try:
            comment = self.get_object()
            self.perform_destroy(comment)
            response = {
                'message': '댓글이 삭제 되었습니다.'
            }

        except ValidationError as e:
            status_code = e.status_code
            is_success = False
            response = {
                'code': e.status_code,
                'message': e.default_detail
            }

        return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

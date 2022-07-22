from rest_framework.views import APIView


class ProfileDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.user:
            pass
        Exception()
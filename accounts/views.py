from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers import ProfileDetailSerializer


class ProfileDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.user:
            print(request.user)
            profile = Profile.objects.get(user=self.request.user.id)
            serializer = ProfileDetailSerializer(profile)
            return Response(serializer.data)
        raise Exception('')

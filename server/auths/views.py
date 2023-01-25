from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User, Profile
from auths.services import (
    google_get_user_info,
    kakao_get_user_info,
    naver_get_user_info, user_create,
)


class KakaoLoginAPI(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def post(self, request, *args, **kwargs):
        access_token = self.request.data['access_token']
        info = kakao_get_user_info(access_token=access_token)
        account = info['kakao_account']
        user: User = user_create(email=account['email'], nickname=account['profile']['nickname'],
                                 profile_image=account['profile'].get('profile_image_url', None),
                                 platform='KAKAO', platform_id=str(info['id']))
        token = TokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        })


class NaverLoginAPI(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def post(self, request, *args, **kwargs):
        access_token = self.request.data['access_token']
        info = naver_get_user_info(access_token=access_token)
        account = info['response']
        user: User = user_create(email=account['email'], nickname=account.get('nickname', None),
                                 profile_image=account.get('profile_image', None),
                                 platform='NAVER', platform_id=account['id'])
        token = TokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        })


class GoogleLoginAPI(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    def post(self, request, *args, **kwargs):
        access_token = self.request.data['access_token']
        info: dict = google_get_user_info(access_token=access_token)
        user = user_create(email=info['email'], nickname=info.get('nickname', None),
                           profile_image=info.get('picture', None),
                           platform='GOOGLE', platform_id=info['sub'])
        token = TokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        })


@api_view(['POST'])
def generate_token(request):
    user = User.objects.create_user(
        username=request.data['username'], email=request.data['email'],
        password=request.data['password']
    )
    Profile.objects.create(user=user)

    token = TokenObtainPairSerializer.get_token(user)
    return Response({
        'refresh_token': str(token),
        'access_token': str(token.access_token)
    })


class TestLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            token = TokenObtainPairSerializer.get_token(user)
            return Response({
                'refresh_token': str(token),
                'access_token': str(token.access_token)
            })
        return Response({

        })

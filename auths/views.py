import os

from django.conf import settings
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User

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
        user = user_create(email=account['email'], nickname=account['profile']['nickname'],
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
        user = user_create(email=account['email'], nickname=account.get('nickname', None),
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
        access_token = request.body['access_token']
        info = google_get_user_info(access_token=access_token)
        user = user_create(email=info['email'], nickname=info['nickname'],
                           profile_image=info.get('picture', None),
                           platform='GOOGLE', platform_id='123')
        token = TokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        })

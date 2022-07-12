import requests
import os
import json

from django.conf import settings
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from auth.services import google_get_access_token, google_get_user_info, kakao_get_access_token, kakao_get_user_info


class KakaoLoginAPI(APIView):
    def get(self, request):
        client_id = os.environ.get('KAKAO_REST_API_KEY')
        redirect_url = settings.BASE_BACKEND_URL + '/api/v1/accounts/kakao/callback/'
        response = redirect(
            f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_url}"
        )
        return response


class KakaoCallbackAPI(APIView):
    def get(self, request):
        auth_code = self.request.GET.get('code')
        url = 'https://kauth.kakao.com/oauth/token'

        access_token = kakao_get_access_token(url, code=auth_code)
        info = kakao_get_user_info(access_token=access_token)
        print(info)

        return Response(1)


class GoogleLoginAPI(APIView):
    def get(self, request, *args, **kwargs):
        app_key = os.environ.get('GOOGLE_CLIENT_ID')
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"

        redirect_uri = settings.BASE_BACKEND_URL + "/api/v1/accounts/google/callback/"
        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"

        response = redirect(
            f"{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
        )

        return response


class GoogleSignInAPI(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        google_token_api = "https://oauth2.googleapis.com/token"

        access_token = google_get_access_token(google_token_api, code)
        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'username': user_data['email'],
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
            'nickname': user_data.get('nickname', ''),
            'name': user_data.get('name', ''),
            'image': user_data.get('picture', None),
            'path': "google",
        }

        print(profile_data)

        return Response(1)

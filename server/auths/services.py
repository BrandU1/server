from __future__ import annotations

import os
from typing import Optional

import requests
from accounts.models import User, Profile
from django.conf import settings
from django.core.exceptions import ValidationError

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def kakao_get_user_info(access_token):
    url = 'https://kapi.kakao.com/v2/user/me'
    response = requests.get(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {access_token}'
    })

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Kakao.')

    user_info = response.json()

    return user_info


def kakao_get_access_token(url, code):
    redirect_url = settings.BASE_BACKEND_URL + '/auth/kakao/callback/'
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.environ.get('KAKAO_REST_API_KEY'),
        'redirect_uri': redirect_url,
        'code': code
    }

    response = requests.post(url, data=data)

    if not response.ok:
        raise ValidationError('kakao_code is invalid')

    access_token = response.json().get('access_token')

    return access_token


def naver_get_access_token(url, code):
    redirect_url = settings.BASE_BACKEND_URL + '/auth/naver/callback/'
    params = {
        'response_type': 'code',
        'grant_type': 'authorization_code',
        'client_id': os.environ.get('NAVER_CLIENT_ID'),
        'client_secret': os.environ.get('NAVER_CLIENT_SECRET'),
        'redirect_uri': redirect_url,
        'code': code,
        'state': 'RANDOM_STATE'
    }

    response = requests.get(url, params=params)

    if not response.ok:
        raise ValidationError('naver_code is invalid')

    access_token = response.json().get('access_token')

    return access_token


def naver_get_user_info(access_token):
    url = 'https://openapi.naver.com/v1/nid/me'
    response = requests.get(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {access_token}'
    })

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Naver.')

    user_info = response.json()

    return user_info


def google_get_access_token(url, code):
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    code = code
    grant_type = 'authorization_code'
    redirection_uri = settings.BASE_BACKEND_URL + "/auth/google/callback/"
    state = "random_string"

    url += \
        f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}" \
        f"&redirect_uri={redirection_uri}&state={state} "

    token_response = requests.post(url)

    if not token_response.ok:
        raise ValidationError('google_token is invalid')

    access_token = token_response.json().get('access_token')

    return access_token


def google_get_user_info(access_token) -> dict:
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        params={
            'access_token': access_token
        }
    )

    if not user_info_response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    user_info = user_info_response.json()

    return user_info


def user_create(email: str, nickname: Optional[str], profile_image: Optional[str], platform: str, platform_id: str):
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            'email': email,
        }
    )

    Profile.create(
        created=created, user=user, nickname=nickname, profile_image=profile_image, platform=platform,
        platform_id=platform_id
    )

    return user

import os
import requests

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
    redirect_url = settings.BASE_BACKEND_URL + '/api/v1/accounts/kakao/callback/'
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
    print(response.json())

    return access_token


def google_get_access_token(url, code):
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    code = code
    grant_type = 'authorization_code'
    redirection_uri = settings.BASE_BACKEND_URL + "/api/v1/accounts/google/callback/"
    state = "random_string"

    url += \
        f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}" \
        f"&redirect_uri={redirection_uri}&state={state} "

    token_response = requests.post(url)

    if not token_response.ok:
        raise ValidationError('google_token is invalid')

    access_token = token_response.json().get('access_token')

    return access_token


def google_get_user_info(access_token):
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

from rest_framework import status
from rest_framework.exceptions import APIException


class KeyDoesNotExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '키가 입력되지 않았습니다. 다시 한번 확인해주세요.'
    default_code = 'KeyNotFound'


class ProfileNotMatchException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '요청하신 데이터의 소유자가 아닙니다.'
    default_code = 'UserNotMatch'

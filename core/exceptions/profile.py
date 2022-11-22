from rest_framework import status
from rest_framework.exceptions import APIException


class ProfileNotAllowException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '자기 자신을 추가하거나 삭제할 수 없습니다.'
    default_code = 'UserNotAllow'


class ProfileNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '해당 프로필이 존재하지 않습니다.'
    default_code = 'ProfileNotExist'

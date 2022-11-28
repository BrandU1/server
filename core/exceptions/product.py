from rest_framework import status
from rest_framework.exceptions import APIException


class RelationAlreadyExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '해당 관계가 이미 존재하기때문에 추가할 수 없습니다.'
    default_code = 'RelationExist'


class RelationDoesNotExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '해당 관계가 존재하지 않기 때문에 삭제할 수 없습니다.'
    default_code = 'RelationNotExist'

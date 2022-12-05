from rest_framework import status
from rest_framework.exceptions import APIException


class OrderAlreadyConfirmException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 구매 확정처리가 된 결제입니다.'
    default_code = 'AlreadyConfirm'


class OrderPaymentAlreadyConfirmException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 결제 확정 처리가 된 결제입니다.'
    default_code = 'AlreadyConfirm'


class OrderPaymentPriceNotEqualException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '결제 금액이 일치하지 않습니다.'
    default_code = 'PriceNotEqual'


class TossPaymentException(APIException):
    def __init__(self, status_code: int, message: str, code: str):
        super().__init__()
        self.status_code = status_code
        self.default_detail = message
        self.default_code = code

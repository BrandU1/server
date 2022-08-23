from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValueError": _handle_generic_error,
        "AttributeError": _handle_generic_error,
    }

    response = exception_handler(exc, context)

    if response is not None:
        response.data["success"] = False
        response.data["status_code"] = response.status_code
        response.data["results"] = response.data["detail"]
        return response

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)


def _handle_generic_error(exc, context, response):
    data = {
        "success": "0",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "results": "서버 에러 입니다. 관리자에게 문의 주세요.",
        "detail": exc.args[0],
    }
    return Response(data)

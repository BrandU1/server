from rest_framework import status
from rest_framework.views import exception_handler

from core.response import brandu_standard_response


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
    is_success = False
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response = {
        "code": exc.__class__.__name__,
        "message": str(exc),
    }
    return brandu_standard_response(is_success=is_success, response=response, status_code=status_code)

from rest_framework.response import Response


def brandu_standard_response(is_success: bool, response: dict, status_code: int, headers=None):
    """Return a standard response for the API.

    param response: The response to return.
    param status_code: The status code to return.
    param headers: The headers to return.
    return: A standard response for the API.
    """
    payload: dict = {}

    if is_success:
        payload['status'] = 'success'
        payload['results'] = response

    else:
        payload['status'] = 'fail'
        payload['error'] = response

    return Response(
        data=payload,
        status=status_code,
        headers=headers
    )

"""
Since DRF 3.x serializers don't call model.full_clean() anymore so models won't be validated properly when the clean
method raises validation errors. The solution for this project is catch any django.core.exceptions.ValidationError and
reraise them as rest_framework.exceptions.ValidationError
"""

from rest_framework.views import exception_handler

from django.core import exceptions as core_ex
from rest_framework import exceptions as rest_ex, status

from kalendario.common.util import NON_FIELD_ERRORS


def custom_exception_handler(exc, context):
    # Transform django core validation exception in rest exception so response is not None
    if isinstance(exc, core_ex.ValidationError):
        # Makes sure that all errors are send as dicts instead of lists, this allows easier handling on the SPA side
        errors = getattr(exc, 'message_dict', {NON_FIELD_ERRORS: exc.messages})
        exc = rest_ex.ValidationError(detail=errors, code=422)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, rest_ex.ValidationError):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        response.data = {'detail': response.data, 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}

    return response

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class SuperheroNotFoundError(Exception):
    pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, SuperheroNotFoundError):
        return Response(
            {'error': str(exc)},
            status=status.HTTP_404_NOT_FOUND
        )

    return response
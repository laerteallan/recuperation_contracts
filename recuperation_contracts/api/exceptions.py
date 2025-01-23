from rest_framework import status


class AppError(Exception):
    """Class Default to Error in application."""
    status_app: int


class ParamInvalid(AppError):
    status_app = status.HTTP_400_BAD_REQUEST


class ObjectNotFound(AppError):
    status_app = status.HTTP_404_NOT_FOUND

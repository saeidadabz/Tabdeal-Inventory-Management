from django.http import Http404
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler


class DomainError(APIException):
    """
    Base class for business-rule errors (e.g. InsufficientStock).

    Subclasses set `status_code`, `default_detail` and `default_code`.
    `details` is optional machine-readable context for API clients.
    """

    def __init__(self, detail=None, details=None):
        super().__init__(detail=detail)
        self.details = details


def api_exception_handler(exc, context):
    """
    Every error response has the same shape:

        {"error": {"code": "...", "message": "...", "details": ...}}
    """
    response = exception_handler(exc, context)
    if response is None:
        return None  # unexpected exception -> Django returns a real 500

    if isinstance(exc, ValidationError):
        code = "validation_error"
        message = "Invalid input."
        details = response.data
    elif isinstance(exc, APIException):
        code = exc.get_codes()
        message = str(exc.detail)
        details = getattr(exc, "details", None)
    else:
        # Django's Http404 / PermissionDenied (converted to a response by DRF)
        code = "not_found" if isinstance(exc, Http404) else "permission_denied"
        message = str(response.data.get("detail", ""))
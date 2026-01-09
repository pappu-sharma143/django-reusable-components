from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that provides consistent error responses.
    
    Returns:
        Response with error details in a consistent format
    """
    
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, handle Django exceptions
    if response is None:
        if isinstance(exc, Http404):
            return Response({
                'error': {
                    'message': 'Resource not found.',
                    'code': 'NOT_FOUND',
                    'details': {}
                }
            }, status=status.HTTP_404_NOT_FOUND)
        
        elif isinstance(exc, PermissionDenied):
            return Response({
                'error': {
                    'message': 'Permission denied.',
                    'code': 'PERMISSION_DENIED',
                    'details': {}
                }
            }, status=status.HTTP_403_FORBIDDEN)
        
        elif isinstance(exc, DjangoValidationError):
            return Response({
                'error': {
                    'message': 'Validation error.',
                    'code': 'VALIDATION_ERROR',
                    'details': exc.message_dict if hasattr(exc, 'message_dict') else {'detail': str(exc)}
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # For unhandled exceptions, return a generic error
            return Response({
                'error': {
                    'message': 'An unexpected error occurred.',
                    'code': 'INTERNAL_ERROR',
                    'details': {'detail': str(exc)}
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Customize the response for DRF exceptions
    if response is not None:
        error_data = {
            'error': {
                'message': get_error_message(response.data),
                'code': get_error_code(exc),
                'details': response.data
            }
        }
        response.data = error_data
    
    return response


def get_error_message(data):
    """Extract a user-friendly error message from response data."""
    
    if isinstance(data, dict):
        # Try to get the first error message
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                return str(value[0])
            elif isinstance(value, str):
                return value
        return 'An error occurred.'
    elif isinstance(data, list) and len(data) > 0:
        return str(data[0])
    else:
        return str(data)


def get_error_code(exc):
    """Get an error code based on the exception type."""
    
    error_codes = {
        'ValidationError': 'VALIDATION_ERROR',
        'ParseError': 'PARSE_ERROR',
        'AuthenticationFailed': 'AUTHENTICATION_FAILED',
        'NotAuthenticated': 'NOT_AUTHENTICATED',
        'PermissionDenied': 'PERMISSION_DENIED',
        'NotFound': 'NOT_FOUND',
        'MethodNotAllowed': 'METHOD_NOT_ALLOWED',
        'NotAcceptable': 'NOT_ACCEPTABLE',
        'UnsupportedMediaType': 'UNSUPPORTED_MEDIA_TYPE',
        'Throttled': 'THROTTLED',
    }
    
    exc_class_name = exc.__class__.__name__
    return error_codes.get(exc_class_name, 'ERROR')


class APIException(Exception):
    """Base exception class for API errors."""
    
    def __init__(self, message, code='ERROR', status_code=status.HTTP_400_BAD_REQUEST, details=None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundException(APIException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, message='Resource not found.', details=None):
        super().__init__(
            message=message,
            code='RESOURCE_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class InvalidRequestException(APIException):
    """Exception raised for invalid requests."""
    
    def __init__(self, message='Invalid request.', details=None):
        super().__init__(
            message=message,
            code='INVALID_REQUEST',
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class UnauthorizedException(APIException):
    """Exception raised for unauthorized access."""
    
    def __init__(self, message='Unauthorized access.', details=None):
        super().__init__(
            message=message,
            code='UNAUTHORIZED',
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class ForbiddenException(APIException):
    """Exception raised for forbidden access."""
    
    def __init__(self, message='Access forbidden.', details=None):
        super().__init__(
            message=message,
            code='FORBIDDEN',
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class ConflictException(APIException):
    """Exception raised for resource conflicts."""
    
    def __init__(self, message='Resource conflict.', details=None):
        super().__init__(
            message=message,
            code='CONFLICT',
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )

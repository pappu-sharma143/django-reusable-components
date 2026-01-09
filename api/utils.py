from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


def success_response(data=None, message='Success', status_code=status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Response object
    """
    response_data = {
        'success': True,
        'message': message,
        'timestamp': timezone.now().isoformat(),
    }
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(message='Error', code='ERROR', details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        code: Error code
        details: Additional error details
        status_code: HTTP status code
        
    Returns:
        Response object
    """
    response_data = {
        'success': False,
        'error': {
            'message': message,
            'code': code,
            'timestamp': timezone.now().isoformat(),
        }
    }
    
    if details:
        response_data['error']['details'] = details
    
    return Response(response_data, status=status_code)


def paginated_response(queryset, serializer_class, request, pagination_class=None):
    """
    Create a paginated response.
    
    Args:
        queryset: Django queryset
        serializer_class: Serializer class to use
        request: Request object
        pagination_class: Pagination class (optional)
        
    Returns:
        Response object
    """
    if pagination_class:
        paginator = pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = serializer_class(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
    
    serializer = serializer_class(queryset, many=True, context={'request': request})
    return Response(serializer.data)


def get_client_ip(request):
    """
    Get the client's IP address from the request.
    
    Args:
        request: Request object
        
    Returns:
        IP address string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Get the user agent from the request.
    
    Args:
        request: Request object
        
    Returns:
        User agent string
    """
    return request.META.get('HTTP_USER_AGENT', '')


def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present in the data.
    
    Args:
        data: Dictionary of data
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, missing_fields)
    """
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    return len(missing_fields) == 0, missing_fields


def clean_query_params(request, allowed_params):
    """
    Extract and clean query parameters from request.
    
    Args:
        request: Request object
        allowed_params: List of allowed parameter names
        
    Returns:
        Dictionary of cleaned parameters
    """
    params = {}
    for param in allowed_params:
        value = request.query_params.get(param)
        if value is not None:
            params[param] = value
    return params


def build_absolute_uri(request, path):
    """
    Build an absolute URI from a path.
    
    Args:
        request: Request object
        path: Relative path
        
    Returns:
        Absolute URI string
    """
    return request.build_absolute_uri(path)


def parse_boolean(value):
    """
    Parse a string value to boolean.
    
    Args:
        value: String value
        
    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    
    return bool(value)


def get_object_or_none(model, **kwargs):
    """
    Get an object or return None if it doesn't exist.
    
    Args:
        model: Django model class
        **kwargs: Filter parameters
        
    Returns:
        Model instance or None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def bulk_create_or_update(model, data, unique_fields):
    """
    Bulk create or update objects.
    
    Args:
        model: Django model class
        data: List of dictionaries with object data
        unique_fields: List of fields that uniquely identify an object
        
    Returns:
        Tuple of (created_count, updated_count)
    """
    created_count = 0
    updated_count = 0
    
    for item in data:
        # Extract unique field values
        unique_values = {field: item[field] for field in unique_fields if field in item}
        
        # Try to get existing object
        obj = get_object_or_none(model, **unique_values)
        
        if obj:
            # Update existing object
            for key, value in item.items():
                setattr(obj, key, value)
            obj.save()
            updated_count += 1
        else:
            # Create new object
            model.objects.create(**item)
            created_count += 1
    
    return created_count, updated_count


def format_validation_errors(errors):
    """
    Format validation errors into a user-friendly format.
    
    Args:
        errors: Validation errors from serializer
        
    Returns:
        Formatted error dictionary
    """
    formatted_errors = {}
    
    for field, messages in errors.items():
        if isinstance(messages, list):
            formatted_errors[field] = messages[0] if messages else 'Invalid value'
        else:
            formatted_errors[field] = str(messages)
    
    return formatted_errors

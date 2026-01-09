# API App

A comprehensive Django REST Framework configuration app with common serializers, pagination, filters, and API utilities.

## Features

- ✅ REST Framework configuration and settings
- ✅ Common base serializers and mixins
- ✅ Custom pagination classes
- ✅ API versioning support
- ✅ Throttling and rate limiting
- ✅ Custom filters and search
- ✅ API documentation (Swagger/ReDoc)
- ✅ CORS configuration
- ✅ JWT authentication support

## Installation

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... other apps
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'drf_yasg',  # For API documentation
]
```

### 2. Add CORS Middleware

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]
```

### 3. REST Framework Configuration

Add to your `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
}
```

### 4. JWT Configuration

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
```

### 5. CORS Configuration

```python
# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# For production, specify allowed origins
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
# ]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### 6. Install Required Packages

```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install django-cors-headers
pip install drf-yasg
pip install markdown
```

### 7. Include URLs

Add to your main `urls.py`:

```python
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # ... other patterns
    path('api/', include('api.urls')),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

## Usage

### Using Base Serializers

```python
from api.serializers import TimestampedSerializer

class MyModelSerializer(TimestampedSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### Using Pagination

```python
from api.pagination import StandardResultsSetPagination, LargeResultsSetPagination

class MyViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    # or
    # pagination_class = LargeResultsSetPagination
```

### Using Custom Filters

```python
from api.filters import CreatedDateFilter

class MyViewSet(viewsets.ModelViewSet):
    filter_backends = [CreatedDateFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
```

### Using Response Utilities

```python
from api.utils import success_response, error_response

def my_view(request):
    data = {'message': 'Success'}
    return success_response(data, status_code=200)
    
    # Or for errors
    return error_response('Something went wrong', status_code=400)
```

### Using Mixins

```python
from api.mixins import TimestampedModelMixin

class MyModel(TimestampedModelMixin):
    name = models.CharField(max_length=100)
    # created_at and updated_at are automatically added
```

## API Endpoints

### JWT Authentication

```
POST /api/token/
{
    "email": "user@example.com",
    "password": "password123"
}
Response: {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

```
POST /api/token/refresh/
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
Response: {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### API Health Check

```
GET /api/health/
Response: {
    "status": "healthy",
    "timestamp": "2026-01-09T10:56:29Z"
}
```

## Components

### Pagination Classes

- `StandardResultsSetPagination` - 20 items per page
- `LargeResultsSetPagination` - 100 items per page
- `SmallResultsSetPagination` - 10 items per page

### Serializers

- `TimestampedSerializer` - Base serializer with created_at/updated_at
- `DynamicFieldsSerializer` - Allows field selection via query params

### Mixins

- `TimestampedModelMixin` - Adds created_at and updated_at fields
- `SoftDeleteMixin` - Adds soft delete functionality

### Filters

- `CreatedDateFilter` - Filter by created date range
- `UpdatedDateFilter` - Filter by updated date range

### Throttling

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

## API Versioning

The API supports versioning through URL path:

```
/api/v1/resource/
/api/v2/resource/
```

## Error Handling

Custom error responses with consistent format:

```json
{
    "error": {
        "message": "Error description",
        "code": "ERROR_CODE",
        "details": {}
    }
}
```

## Best Practices

1. **Always use serializers** for data validation
2. **Implement proper permissions** on all endpoints
3. **Use pagination** for list endpoints
4. **Add filtering and search** for better UX
5. **Version your API** for backward compatibility
6. **Document your endpoints** using Swagger/ReDoc
7. **Implement rate limiting** to prevent abuse
8. **Use HTTPS** in production
9. **Validate all inputs** before processing
10. **Return appropriate HTTP status codes**

## Testing

Run tests:

```bash
python manage.py test api
```

## Documentation

Access API documentation:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Troubleshooting

### Issue: CORS errors
- Check CORS_ALLOWED_ORIGINS configuration
- Ensure corsheaders middleware is at the top
- Verify frontend origin is allowed

### Issue: JWT token expired
- Check ACCESS_TOKEN_LIFETIME setting
- Use refresh token to get new access token
- Implement token refresh logic in frontend

### Issue: Rate limit exceeded
- Adjust DEFAULT_THROTTLE_RATES
- Implement custom throttle classes
- Use caching for frequently accessed data

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

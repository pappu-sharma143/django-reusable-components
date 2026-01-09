# Authentication App

A comprehensive Django authentication app with custom user models, social authentication, and two-factor authentication (2FA).

## Features

- ✅ Custom User Model with email-based authentication
- ✅ Social Authentication (Google, Facebook, GitHub)
- ✅ Two-Factor Authentication (2FA) with TOTP
- ✅ Email verification
- ✅ Password reset functionality
- ✅ JWT token authentication for APIs
- ✅ User profile management
- ✅ Role-based permissions

## Installation

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... other apps
    'authentication',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'django_otp',
    'django_otp.plugins.otp_totp',
]
```

### 2. Set Custom User Model

Add to your `settings.py`:

```python
AUTH_USER_MODEL = 'authentication.User'
```

### 3. Configure Authentication Backends

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

### 4. Email Configuration

```python
# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use SMTP
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
```

### 5. Social Auth Configuration

```python
# Google OAuth2
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
        ],
    },
    'github': {
        'SCOPE': [
            'user',
            'email',
        ],
    }
}

# Add your OAuth credentials
SOCIALACCOUNT_GOOGLE_CLIENT_ID = 'your-google-client-id'
SOCIALACCOUNT_GOOGLE_SECRET = 'your-google-secret'
```

### 6. Django Allauth Settings

```python
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
```

### 7. Install Required Packages

```bash
pip install djangorestframework
pip install django-allauth
pip install django-otp
pip install qrcode
pip install pillow
```

### 8. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Include URLs

Add to your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... other patterns
    path('auth/', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),
]
```

## Usage

### Custom User Model

The custom user model uses email as the primary identifier:

```python
from authentication.models import User

# Create a user
user = User.objects.create_user(
    email='user@example.com',
    password='securepassword123',
    first_name='John',
    last_name='Doe'
)

# Create a superuser
superuser = User.objects.create_superuser(
    email='admin@example.com',
    password='adminpassword123'
)
```

### Two-Factor Authentication (2FA)

#### Enable 2FA for a User

```python
from authentication.services import TwoFactorService

# Generate QR code for user
service = TwoFactorService()
qr_code_url = service.enable_2fa(user)
# Display qr_code_url to user to scan with authenticator app
```

#### Verify 2FA Token

```python
from authentication.services import TwoFactorService

service = TwoFactorService()
is_valid = service.verify_2fa_token(user, token='123456')
```

### Social Authentication

Users can authenticate using:
- Google OAuth2
- Facebook OAuth2
- GitHub OAuth2

The social authentication is handled automatically by django-allauth.

### API Endpoints

#### Register
```
POST /auth/register/
{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login
```
POST /auth/login/
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

#### Enable 2FA
```
POST /auth/2fa/enable/
Headers: Authorization: Token <your-token>
```

#### Verify 2FA
```
POST /auth/2fa/verify/
{
    "token": "123456"
}
Headers: Authorization: Token <your-token>
```

#### Disable 2FA
```
POST /auth/2fa/disable/
Headers: Authorization: Token <your-token>
```

#### Get User Profile
```
GET /auth/profile/
Headers: Authorization: Token <your-token>
```

#### Update User Profile
```
PATCH /auth/profile/
{
    "first_name": "Jane",
    "phone_number": "+1234567890"
}
Headers: Authorization: Token <your-token>
```

## Models

### User Model

Fields:
- `email` (EmailField, unique) - Primary identifier
- `first_name` (CharField)
- `last_name` (CharField)
- `phone_number` (CharField, optional)
- `is_email_verified` (BooleanField)
- `is_2fa_enabled` (BooleanField)
- `date_joined` (DateTimeField)
- `is_active` (BooleanField)
- `is_staff` (BooleanField)
- `is_superuser` (BooleanField)

### UserProfile Model

Extended profile information:
- `user` (OneToOneField to User)
- `bio` (TextField)
- `avatar` (ImageField)
- `date_of_birth` (DateField)
- `address` (TextField)
- `city` (CharField)
- `country` (CharField)
- `postal_code` (CharField)

## Services

### TwoFactorService

Handles all 2FA operations:
- `enable_2fa(user)` - Enable 2FA and generate QR code
- `disable_2fa(user)` - Disable 2FA for user
- `verify_2fa_token(user, token)` - Verify TOTP token
- `generate_backup_codes(user)` - Generate backup codes

### EmailService

Handles email operations:
- `send_verification_email(user)` - Send email verification
- `send_password_reset_email(user)` - Send password reset email
- `send_welcome_email(user)` - Send welcome email

## Security Best Practices

1. **Password Validation**: Uses Django's built-in password validators
2. **Email Verification**: Mandatory email verification for new accounts
3. **2FA Support**: Optional TOTP-based two-factor authentication
4. **Token Authentication**: Secure token-based authentication for APIs
5. **HTTPS Only**: Always use HTTPS in production
6. **Rate Limiting**: Implement rate limiting on authentication endpoints

## Testing

Run tests:

```bash
python manage.py test authentication
```

## Troubleshooting

### Issue: Email not sending
- Check EMAIL_BACKEND configuration
- Verify SMTP credentials
- Check firewall/network settings

### Issue: Social auth not working
- Verify OAuth credentials
- Check redirect URIs in OAuth provider settings
- Ensure HTTPS is enabled in production

### Issue: 2FA QR code not displaying
- Install qrcode and pillow packages
- Check media file configuration
- Verify MEDIA_URL and MEDIA_ROOT settings

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

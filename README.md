# Django Components Library

A comprehensive, production-ready collection of reusable Django components, apps, and utilities.

## 📦 Overview

This library provides a complete set of Django components organized into self-contained apps and modules. Each component is documented, tested, and ready for production use.

## 🏗️ Project Structure

```
django-components/
├── authentication/          # Custom user models, social auth, 2FA
├── api/                     # REST framework configurations
├── core/                    # Base models, mixins, utilities
│   ├── validators/         # Custom validators
│   ├── mixins/             # Model mixins
│   ├── managers/           # Custom managers
│   ├── utils/              # Utility functions
│   ├── middleware/         # Custom middleware
│   ├── templatetags/       # Template tags & filters
│   ├── decorators/         # Custom decorators
│   └── signals/            # Signal handlers
├── payments/                # Stripe/PayPal integration
├── notifications/           # Email, SMS, push notifications
├── forms/                   # Form components
│   ├── mixins/             # Form mixins
│   ├── fields/             # Custom form fields
│   └── widgets/            # Custom widgets
└── config/                  # Project configuration
```

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd django-components
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure settings:**
```python
# settings.py
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'django_filters',
    'corsheaders',
    
    # Custom apps
    'authentication',
    'api',
    'core',
    'payments',
    'notifications',
]

# Set custom user model
AUTH_USER_MODEL = 'authentication.User'
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

## 📚 Apps & Components

### 1. Authentication App
**Location:** `authentication/`

**Features:**
- Custom user model with email authentication
- Social authentication (Google, Facebook, GitHub)
- Two-factor authentication (2FA) with TOTP
- Email verification
- Password reset
- JWT token authentication
- User profile management

**[View Documentation](authentication/README.md)**

### 2. API App
**Location:** `api/`

**Features:**
- REST Framework configuration
- Common serializers and mixins
- Custom pagination classes
- API versioning
- Throttling and rate limiting
- Custom filters
- API documentation (Swagger/ReDoc)
- CORS configuration

**[View Documentation](api/README.md)**

### 3. Core App
**Location:** `core/`

**Features:**
- Base abstract models
- Model mixins (timestamps, soft delete, etc.)
- Custom model managers
- Utility functions
- Template tags and filters
- Middleware components
- Custom validators
- Signal handlers

**[View Documentation](core/README.md)**

### 4. Payments App
**Location:** `payments/`

**Features:**
- Stripe integration
- PayPal integration
- Payment tracking
- Subscription management
- Invoice generation
- Webhook handling
- Refund processing

**[View Documentation](payments/README.md)**

### 5. Notifications App
**Location:** `notifications/`

**Features:**
- Email notifications
- SMS notifications (Twilio)
- Push notifications (Firebase, OneSignal)
- In-app notifications
- Slack notifications
- Notification templates
- Batch notifications

**[View Documentation](notifications/README.md)**

## 🧩 Component Categories

### Models & Database

#### Abstract Base Models
- `TimeStampedModel` - created_at, updated_at
- `SoftDeleteModel` - soft delete functionality
- `UUIDModel` - UUID primary key
- `PublishableModel` - publishing workflow
- `OrderableModel` - manual ordering
- `SlugModel` - auto-generating slugs
- `SEOModel` - SEO metadata

#### Model Mixins
- `TimestampedModelMixin`
- `SoftDeleteMixin`
- `PublishableMixin`
- `OrderableMixin`
- `SlugMixin`
- `ViewCountMixin`
- `LikableMixin`
- `RatableMixin`

#### Custom Managers
- `SoftDeleteManager` - filter deleted items
- `PublishedManager` - filter published items
- `ActiveManager` - filter active items
- `ViewCountManager` - most viewed queries
- `RatingManager` - top rated queries
- `TimeRangeManager` - date-based queries

**[View Models Documentation](core/README.md#models)**

### Validators

Comprehensive validators for:
- Phone numbers
- Email domains
- File sizes and extensions
- Image dimensions
- Dates and age ranges
- Credit cards
- Postal codes
- Passwords
- URLs, IPs, colors
- JSON structure

**[View Validators Documentation](core/validators/README.md)**

### Forms & Fields

#### Form Mixins
- `BootstrapFormMixin` - Bootstrap styling
- `PlaceholderFormMixin` - auto placeholders
- `DisabledFieldsMixin`
- `ReadOnlyFieldsMixin`
- `AjaxFormMixin`

#### Custom Fields
- `PhoneNumberField`
- `ColorPickerField`
- `PriceField`
- `PercentageField`

#### Custom Widgets
- `DatePickerWidget`
- `ColorPickerWidget`
- `RichTextEditorWidget`
- `AutocompleteWidget`

### API Components

#### Serializers
- `TimestampedSerializer`
- `DynamicFieldsSerializer`
- `BulkCreateSerializer`
- `FileUploadSerializer`
- `ImageUploadSerializer`

#### Pagination
- `StandardResultsSetPagination` (20 items)
- `LargeResultsSetPagination` (100 items)
- `CustomCursorPagination`
- `InfinitePagination`

#### Permissions
- `IsOwnerOrReadOnly`
- `IsAdminOrReadOnly`
- `IsVerifiedUser`
- `IsOwnerOrAdmin`

**[View API Documentation](api/README.md)**

### Utilities

#### String Utilities
- `generate_unique_slug()`
- `truncate_text()`
- `slugify_custom()`

#### Date Utilities
- `get_date_range()`
- `time_ago()`
- `get_month_range()`

#### File Utilities
- `get_file_extension()`
- `generate_filename()`
- `get_file_size_mb()`

#### Email Utilities
- `send_email_template()`
- `send_bulk_email()`

**[View Utils Documentation](core/README.md#utilities)**

### Template Tags & Filters

#### Filters
- `{{ value|currency }}` - format currency
- `{{ value|time_ago }}` - "2 hours ago"
- `{{ value|smart_truncate:100 }}` - smart truncation
- `{{ value|highlight:term }}` - highlight search

#### Tags
- `{% breadcrumb %}` - breadcrumb navigation
- `{% pagination %}` - pagination widget
- `{% cache_buster 'file.css' %}` - cache busting

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token

# Firebase
FIREBASE_SERVER_KEY=your-firebase-key
```

### Settings Modules

```python
# config/settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

## 📖 Usage Examples

### Using Base Models

```python
from core.models import TimeStampedModel, SoftDeleteModel

class Article(TimeStampedModel, SoftDeleteModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Automatically includes:
    # - created_at, updated_at
    # - is_deleted, deleted_at
    # - soft delete methods
```

### Using Validators

```python
from core.validators import validate_phone_number, validate_file_size

class UserProfile(models.Model):
    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )
    document = models.FileField(
        validators=[validate_file_size(max_mb=5)]
    )
```

### Using API Serializers

```python
from api.serializers import TimestampedSerializer

class ArticleSerializer(TimestampedSerializer):
    class Meta:
        model = Article
        fields = '__all__'
```

### Using Mixins

```python
from core.mixins import TimestampedModelMixin, SlugMixin

class Post(TimestampedModelMixin, SlugMixin):
    title = models.CharField(max_length=200)
    # Automatically includes timestamps and slug generation
```

## 🧪 Testing

Run all tests:

```bash
python manage.py test
```

Run specific app tests:

```bash
python manage.py test authentication
python manage.py test api
python manage.py test core
```

## 📦 Dependencies

### Core Dependencies
- Django >= 4.2
- djangorestframework
- django-filter
- django-cors-headers

### Authentication
- django-allauth
- django-otp
- djangorestframework-simplejwt

### Payments
- stripe
- paypalrestsdk

### Notifications
- twilio
- firebase-admin
- slack-sdk

### Development
- pytest
- pytest-django
- factory-boy
- faker

## 🔐 Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use HTTPS** in production
3. **Enable CSRF protection**
4. **Implement rate limiting**
5. **Validate all inputs**
6. **Use parameterized queries**
7. **Keep dependencies updated**
8. **Enable security headers**

## 📈 Performance Tips

1. **Use select_related and prefetch_related**
2. **Implement caching** for frequently accessed data
3. **Use database indexes** appropriately
4. **Optimize queries** with query analysis
5. **Use pagination** for large datasets
6. **Compress static files**
7. **Use CDN** for static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: [View docs]
- Email: support@example.com

## 🗺️ Roadmap

### Completed ✅
- Authentication with 2FA
- REST API framework
- Payment integrations
- Notification system
- Core utilities and mixins

### In Progress 🚧
- Advanced search functionality
- Real-time notifications
- Analytics integration
- Advanced caching strategies

### Planned 📋
- GraphQL API support
- Microservices architecture
- Advanced monitoring
- Multi-tenancy support
- Internationalization (i18n)

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Best Practices Guide](docs/best-practices.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment.md)

---

**Built with ❤️ for the Django community**

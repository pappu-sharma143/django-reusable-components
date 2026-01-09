# Core App

A comprehensive Django core/common app with base models, mixins, utilities, and reusable components.

## Features

- ✅ Base abstract models with common fields
- ✅ Model mixins for timestamps, soft delete, ordering
- ✅ Custom model managers
- ✅ Utility functions and helpers
- ✅ Custom template tags and filters
- ✅ Middleware components
- ✅ Custom validators
- ✅ Signal handlers

## Installation

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... other apps
    'core',
]
```

### 2. Add Middleware (Optional)

```python
MIDDLEWARE = [
    # ... other middleware
    'core.middleware.RequestLoggingMiddleware',
    'core.middleware.TimezoneMiddleware',
]
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Usage

### Using Base Models

```python
from core.models import TimeStampedModel, SoftDeleteModel

class MyModel(TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=100)
    # created_at, updated_at, is_deleted, deleted_at are automatically added
```

### Using Mixins

```python
from core.mixins import TimestampedModelMixin, SoftDeleteMixin, OrderableMixin

class Article(TimestampedModelMixin, SoftDeleteMixin, OrderableMixin):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

### Using Custom Managers

```python
from core.managers import SoftDeleteManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    
    objects = SoftDeleteManager()
    
    # Usage:
    # Post.objects.all()  # Returns only non-deleted posts
    # Post.objects.deleted()  # Returns only deleted posts
    # Post.objects.with_deleted()  # Returns all posts
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
        upload_to='documents/',
        validators=[validate_file_size(max_mb=5)]
    )
```

### Using Utility Functions

```python
from core.utils import generate_unique_slug, send_notification

# Generate unique slug
slug = generate_unique_slug(MyModel, 'My Article Title')

# Send notification
send_notification(
    user=user,
    title='New Message',
    message='You have a new message',
    notification_type='info'
)
```

### Using Template Tags

In your template:

```django
{% load core_tags %}

<!-- Format currency -->
{{ amount|currency }}

<!-- Truncate text -->
{{ long_text|smart_truncate:100 }}

<!-- Time ago -->
{{ created_at|time_ago }}

<!-- Highlight search term -->
{{ text|highlight:search_term }}
```

## Components

### Base Models

#### TimeStampedModel
Abstract model with `created_at` and `updated_at` fields.

```python
class MyModel(TimeStampedModel):
    name = models.CharField(max_length=100)
```

#### SoftDeleteModel
Abstract model with soft delete functionality.

```python
class MyModel(SoftDeleteModel):
    name = models.CharField(max_length=100)
    
    # Usage:
    # obj.delete()  # Soft delete (sets is_deleted=True)
    # obj.hard_delete()  # Permanent delete
    # obj.restore()  # Restore soft-deleted object
```

#### UUIDModel
Abstract model with UUID as primary key.

```python
class MyModel(UUIDModel):
    name = models.CharField(max_length=100)
    # id field is automatically a UUID
```

### Mixins

#### TimestampedModelMixin
Adds `created_at` and `updated_at` fields.

#### SoftDeleteMixin
Adds soft delete functionality with `is_deleted` and `deleted_at` fields.

#### OrderableMixin
Adds `order` field for manual ordering.

#### PublishableMixin
Adds `is_published` and `published_at` fields.

#### SlugMixin
Adds `slug` field with automatic generation.

### Managers

#### SoftDeleteManager
Custom manager that filters out soft-deleted objects by default.

```python
Model.objects.all()  # Excludes deleted
Model.objects.deleted()  # Only deleted
Model.objects.with_deleted()  # All objects
```

#### PublishedManager
Custom manager that filters only published objects.

```python
Model.objects.published()  # Only published
Model.objects.unpublished()  # Only unpublished
```

### Validators

- `validate_phone_number` - Validates phone number format
- `validate_file_size(max_mb)` - Validates file size
- `validate_image_dimensions(min_width, min_height)` - Validates image dimensions
- `validate_alphanumeric` - Validates alphanumeric strings
- `validate_no_special_chars` - Validates strings without special characters

### Utility Functions

#### String Utilities
- `generate_unique_slug(model, title, slug_field='slug')` - Generate unique slug
- `truncate_text(text, length, suffix='...')` - Truncate text smartly
- `slugify_unique(text)` - Create URL-friendly slug

#### Date Utilities
- `get_date_range(start_date, end_date)` - Get list of dates in range
- `get_month_range(date)` - Get start and end of month
- `get_week_range(date)` - Get start and end of week
- `time_ago(date)` - Convert date to "time ago" format

#### File Utilities
- `get_file_extension(filename)` - Get file extension
- `generate_filename(instance, filename)` - Generate unique filename
- `get_file_size_mb(file)` - Get file size in MB

#### Notification Utilities
- `send_notification(user, title, message, type)` - Send notification
- `send_bulk_notification(users, title, message, type)` - Send to multiple users

### Middleware

#### RequestLoggingMiddleware
Logs all incoming requests with details.

#### TimezoneMiddleware
Sets timezone based on user preferences.

#### CorsMiddleware
Handles CORS headers (alternative to django-cors-headers).

### Template Tags

#### Filters
- `currency` - Format number as currency
- `smart_truncate:length` - Smart text truncation
- `time_ago` - Convert to "X time ago" format
- `highlight:term` - Highlight search term in text
- `markdown` - Convert markdown to HTML

#### Tags
- `{% get_settings 'KEY' %}` - Get settings value
- `{% get_env 'KEY' %}` - Get environment variable
- `{% cache_bust 'file.css' %}` - Add cache busting parameter

## Best Practices

1. **Use base models** for common functionality
2. **Leverage mixins** instead of repeating code
3. **Use custom managers** for common queries
4. **Validate data** using custom validators
5. **Keep utilities generic** and reusable
6. **Document your code** for team members
7. **Write tests** for custom functionality

## Testing

Run tests:

```bash
python manage.py test core
```

## Examples

### Complete Model Example

```python
from core.models import TimeStampedModel, SoftDeleteModel
from core.mixins import SlugMixin, PublishableMixin
from core.managers import SoftDeleteManager, PublishedManager

class Article(TimeStampedModel, SoftDeleteModel, SlugMixin, PublishableMixin):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    objects = SoftDeleteManager()
    published_objects = PublishedManager()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    
    def __str__(self):
        return self.title
```

### Using Utilities

```python
from core.utils import generate_unique_slug, send_notification, time_ago

# Generate slug
article.slug = generate_unique_slug(Article, article.title)

# Send notification
send_notification(
    user=article.author,
    title='Article Published',
    message=f'Your article "{article.title}" has been published!',
    notification_type='success'
)

# Display time ago
print(time_ago(article.created_at))  # "2 hours ago"
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

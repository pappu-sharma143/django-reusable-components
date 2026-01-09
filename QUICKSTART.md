# Quick Start Guide

Get started with Django Components in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Basic Django knowledge

## Installation

### 1. Clone or Download

```bash
cd django-components
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install core dependencies only (minimal setup)
pip install Django djangorestframework django-filter django-cors-headers

# OR install all dependencies (full setup)
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

When prompted, enter:
- Email: admin@example.com
- Password: (your secure password)

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## First Steps

### 1. Test Authentication

```python
# Create a test user
from authentication.models import User

user = User.objects.create_user(
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User'
)
print(f"Created user: {user.email}")
```

### 2. Use Base Models

```python
# In your app's models.py
from core.models import TimeStampedModel, SoftDeleteModel

class Article(TimeStampedModel, SoftDeleteModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.title
```

### 3. Use Validators

```python
# In your models.py
from django.db import models
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

### 4. Create an API Endpoint

```python
# In your app's serializers.py
from rest_framework import serializers
from api.serializers import TimestampedSerializer
from .models import Article

class ArticleSerializer(TimestampedSerializer):
    class Meta:
        model = Article
        fields = '__all__'

# In your app's views.py
from rest_framework import viewsets
from api.pagination import StandardResultsSetPagination
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination

# In your app's urls.py
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register('articles', ArticleViewSet)

urlpatterns = router.urls
```

### 5. Test the API

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"yourpassword"}'

# Use the token
curl http://localhost:8000/api/articles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Common Tasks

### Create a New App

```bash
python manage.py startapp myapp
```

Add to `INSTALLED_APPS` in `config/settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'myapp',
]
```

### Use Soft Delete

```python
from core.models import SoftDeleteModel

class Post(SoftDeleteModel):
    title = models.CharField(max_length=200)

# Usage
post = Post.objects.create(title="My Post")
post.delete()  # Soft delete
print(post.is_deleted)  # True

post.restore()  # Restore
print(post.is_deleted)  # False

post.hard_delete()  # Permanent delete
```

### Use Custom Managers

```python
from core.managers import SoftDeleteManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    
    objects = SoftDeleteManager()

# Usage
Post.objects.all()  # Only non-deleted
Post.objects.deleted()  # Only deleted
Post.objects.with_deleted()  # All posts
```

### Send Notifications

```python
from core.models import Notification

# Create notification
Notification.objects.create(
    user=user,
    title='Welcome!',
    message='Thanks for joining',
    notification_type='success'
)

# Get unread notifications
unread = Notification.objects.filter(
    user=user,
    is_read=False
)
```

## Next Steps

1. **Read the Documentation**
   - [Main README](README.md)
   - [Authentication Guide](authentication/README.md)
   - [API Guide](api/README.md)
   - [Core Components](core/README.md)

2. **Explore Examples**
   - Check each app's README for detailed examples
   - Review the models in `core/models.py`
   - Look at serializers in `api/serializers.py`

3. **Customize**
   - Modify settings in `config/settings.py`
   - Add your own apps
   - Extend base models and mixins

4. **Deploy**
   - Set up production database
   - Configure email settings
   - Set up static files
   - Enable HTTPS

## Troubleshooting

### Issue: Import errors

**Solution:** Make sure all apps are in `INSTALLED_APPS`

### Issue: Migration errors

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: CORS errors

**Solution:** Check `CORS_ALLOWED_ORIGINS` in settings.py

## Getting Help

- Check [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for component status
- Review individual app README files
- Check Django documentation: https://docs.djangoproject.com/

## What's Next?

- Set up payment integration (see [payments/README.md](payments/README.md))
- Configure notifications (see [notifications/README.md](notifications/README.md))
- Add two-factor authentication
- Implement social login
- Create custom validators
- Build your API

---

**Happy Coding! 🚀**

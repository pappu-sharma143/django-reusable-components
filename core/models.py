import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """
    Abstract base model that provides soft delete functionality.
    """
    
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete the object."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def hard_delete(self):
        """Permanently delete the object."""
        super().delete()
    
    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class UUIDModel(models.Model):
    """
    Abstract base model that uses UUID as primary key.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """
    Abstract base model for publishable content.
    """
    
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def publish(self):
        """Publish the object."""
        self.is_published = True
        self.published_at = timezone.now()
        self.save()
    
    def unpublish(self):
        """Unpublish the object."""
        self.is_published = False
        self.published_at = None
        self.save()


class OrderableModel(models.Model):
    """
    Abstract base model for manually orderable objects.
    """
    
    order = models.IntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['order', '-id']


class SlugModel(models.Model):
    """
    Abstract base model that provides a slug field.
    """
    
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, 'title'):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SEOModel(models.Model):
    """
    Abstract base model for SEO metadata.
    """
    
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDModel, SoftDeleteModel):
    """
    Complete base model with timestamps, UUID, and soft delete.
    """
    
    class Meta:
        abstract = True


class Notification(TimeStampedModel):
    """
    Model for user notifications.
    """
    
    NOTIFICATION_TYPES = (
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='info'
    )
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    link = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f'{self.user.email} - {self.title}'
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class Setting(models.Model):
    """
    Model for application settings.
    """
    
    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['key']
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
    
    def __str__(self):
        return f'{self.key}: {self.value[:50]}'
    
    @classmethod
    def get_value(cls, key, default=None):
        """Get setting value by key."""
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_value(cls, key, value, description=''):
        """Set or update setting value."""
        setting, created = cls.objects.update_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        return setting


class ActivityLog(TimeStampedModel):
    """
    Model for logging user activities.
    """
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )
    action = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]
    
    def __str__(self):
        user_email = self.user.email if self.user else 'Anonymous'
        return f'{user_email} - {self.action}'

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimestampedModelMixin(models.Model):
    """
    Mixin that adds created_at and updated_at timestamp fields.
    """
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Mixin that adds soft delete functionality.
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


class PublishableMixin(models.Model):
    """
    Mixin for publishable content.
    """
    
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def publish(self):
        """Publish the object."""
        self.is_published = True
        if not self.published_at:
            self.published_at = timezone.now()
        self.save()
    
    def unpublish(self):
        """Unpublish the object."""
        self.is_published = False
        self.save()


class OrderableMixin(models.Model):
    """
    Mixin for manually orderable objects.
    """
    
    order = models.IntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['order']


class SlugMixin(models.Model):
    """
    Mixin that adds a slug field with automatic generation.
    Requires the model to have a 'title' or 'name' field.
    """
    
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Try to get title or name field
            source_field = getattr(self, 'title', None) or getattr(self, 'name', None)
            if source_field:
                self.slug = self._generate_unique_slug(source_field)
        super().save(*args, **kwargs)
    
    def _generate_unique_slug(self, text):
        """Generate a unique slug."""
        slug = slugify(text)
        unique_slug = slug
        num = 1
        
        while self.__class__.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        
        return unique_slug


class SEOMixin(models.Model):
    """
    Mixin for SEO metadata fields.
    """
    
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    class Meta:
        abstract = True


class ActivatableMixin(models.Model):
    """
    Mixin for objects that can be activated/deactivated.
    """
    
    is_active = models.BooleanField(default=True, db_index=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def activate(self):
        """Activate the object."""
        self.is_active = True
        self.activated_at = timezone.now()
        self.deactivated_at = None
        self.save()
    
    def deactivate(self):
        """Deactivate the object."""
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save()


class ViewCountMixin(models.Model):
    """
    Mixin to track view count.
    """
    
    view_count = models.PositiveIntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
    
    def increment_view_count(self):
        """Increment the view count."""
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])
        self.refresh_from_db()


class LikableMixin(models.Model):
    """
    Mixin to track likes/favorites.
    """
    
    like_count = models.PositiveIntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
    
    def increment_likes(self):
        """Increment the like count."""
        self.like_count = models.F('like_count') + 1
        self.save(update_fields=['like_count'])
        self.refresh_from_db()
    
    def decrement_likes(self):
        """Decrement the like count."""
        if self.like_count > 0:
            self.like_count = models.F('like_count') - 1
            self.save(update_fields=['like_count'])
            self.refresh_from_db()


class CommentableMixin(models.Model):
    """
    Mixin to track comment count.
    """
    
    comment_count = models.PositiveIntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
    
    def increment_comments(self):
        """Increment the comment count."""
        self.comment_count = models.F('comment_count') + 1
        self.save(update_fields=['comment_count'])
        self.refresh_from_db()
    
    def decrement_comments(self):
        """Decrement the comment count."""
        if self.comment_count > 0:
            self.comment_count = models.F('comment_count') - 1
            self.save(update_fields=['comment_count'])
            self.refresh_from_db()


class RatableMixin(models.Model):
    """
    Mixin for rating functionality.
    """
    
    rating_sum = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    
    class Meta:
        abstract = True
    
    def add_rating(self, rating):
        """Add a rating and update average."""
        self.rating_sum += rating
        self.rating_count += 1
        self.average_rating = self.rating_sum / self.rating_count
        self.save(update_fields=['rating_sum', 'rating_count', 'average_rating'])
    
    def update_average_rating(self):
        """Recalculate average rating from related ratings."""
        # This should be implemented based on your rating model
        pass

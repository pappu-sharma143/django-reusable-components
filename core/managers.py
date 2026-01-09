from django.db import models


class SoftDeleteManager(models.Manager):
    """
    Manager that filters out soft-deleted objects by default.
    """
    
    def get_queryset(self):
        """Return only non-deleted objects."""
        return super().get_queryset().filter(is_deleted=False)
    
    def deleted(self):
        """Return only deleted objects."""
        return super().get_queryset().filter(is_deleted=True)
    
    def with_deleted(self):
        """Return all objects including deleted ones."""
        return super().get_queryset()
    
    def hard_delete(self):
        """Permanently delete all objects in queryset."""
        return self.get_queryset().delete()


class PublishedManager(models.Manager):
    """
    Manager that returns only published objects.
    """
    
    def get_queryset(self):
        """Return only published objects."""
        return super().get_queryset().filter(is_published=True)
    
    def unpublished(self):
        """Return only unpublished objects."""
        return super().get_queryset().filter(is_published=False)
    
    def all_objects(self):
        """Return all objects regardless of published status."""
        return super().get_queryset()


class ActiveManager(models.Manager):
    """
    Manager that returns only active objects.
    """
    
    def get_queryset(self):
        """Return only active objects."""
        return super().get_queryset().filter(is_active=True)
    
    def inactive(self):
        """Return only inactive objects."""
        return super().get_queryset().filter(is_active=False)
    
    def all_objects(self):
        """Return all objects regardless of active status."""
        return super().get_queryset()


class OrderedManager(models.Manager):
    """
    Manager that returns objects ordered by the 'order' field.
    """
    
    def get_queryset(self):
        """Return objects ordered by order field."""
        return super().get_queryset().order_by('order', '-created_at')


class ViewCountManager(models.Manager):
    """
    Manager with methods for view count operations.
    """
    
    def most_viewed(self, limit=10):
        """Return most viewed objects."""
        return self.get_queryset().order_by('-view_count')[:limit]
    
    def trending(self, days=7, limit=10):
        """Return trending objects based on recent views."""
        from django.utils import timezone
        from datetime import timedelta
        
        date_from = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(
            created_at__gte=date_from
        ).order_by('-view_count')[:limit]


class RatingManager(models.Manager):
    """
    Manager with methods for rating operations.
    """
    
    def top_rated(self, limit=10):
        """Return top rated objects."""
        return self.get_queryset().order_by('-average_rating', '-rating_count')[:limit]
    
    def highly_rated(self, min_rating=4.0, min_count=5):
        """Return highly rated objects with minimum rating and count."""
        return self.get_queryset().filter(
            average_rating__gte=min_rating,
            rating_count__gte=min_count
        ).order_by('-average_rating')


class TimeRangeManager(models.Manager):
    """
    Manager with methods for time-based queries.
    """
    
    def today(self):
        """Return objects created today."""
        from django.utils import timezone
        today = timezone.now().date()
        return self.get_queryset().filter(created_at__date=today)
    
    def this_week(self):
        """Return objects created this week."""
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now()
        week_ago = today - timedelta(days=7)
        return self.get_queryset().filter(created_at__gte=week_ago)
    
    def this_month(self):
        """Return objects created this month."""
        from django.utils import timezone
        
        today = timezone.now()
        return self.get_queryset().filter(
            created_at__year=today.year,
            created_at__month=today.month
        )
    
    def this_year(self):
        """Return objects created this year."""
        from django.utils import timezone
        
        today = timezone.now()
        return self.get_queryset().filter(created_at__year=today.year)
    
    def date_range(self, start_date, end_date):
        """Return objects created within date range."""
        return self.get_queryset().filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )


class SearchableManager(models.Manager):
    """
    Manager with search functionality.
    """
    
    def search(self, query, fields):
        """
        Search for query in specified fields.
        
        Args:
            query: Search query string
            fields: List of field names to search in
            
        Returns:
            Queryset with matching objects
        """
        from django.db.models import Q
        
        if not query:
            return self.get_queryset()
        
        q_objects = Q()
        for field in fields:
            q_objects |= Q(**{f'{field}__icontains': query})
        
        return self.get_queryset().filter(q_objects).distinct()


class BulkManager(models.Manager):
    """
    Manager with bulk operation methods.
    """
    
    def bulk_create_or_update(self, objects, unique_fields, update_fields):
        """
        Bulk create or update objects.
        
        Args:
            objects: List of model instances
            unique_fields: Fields that uniquely identify an object
            update_fields: Fields to update if object exists
        """
        # This is a simplified version
        # For production, consider using django-bulk-update or similar
        created = []
        updated = []
        
        for obj in objects:
            # Build filter kwargs from unique fields
            filter_kwargs = {field: getattr(obj, field) for field in unique_fields}
            
            # Try to get existing object
            try:
                existing = self.get(**filter_kwargs)
                # Update fields
                for field in update_fields:
                    setattr(existing, field, getattr(obj, field))
                existing.save()
                updated.append(existing)
            except self.model.DoesNotExist:
                obj.save()
                created.append(obj)
        
        return created, updated

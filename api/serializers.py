from rest_framework import serializers
from django.utils import timezone


class TimestampedSerializer(serializers.ModelSerializer):
    """
    Base serializer that includes created_at and updated_at fields.
    Use this as a base for models that have timestamp fields.
    """
    
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that allows dynamic field selection via query parameters.
    
    Usage:
        /api/resource/?fields=id,name,email
    """
    
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields.split(','))
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ReadOnlySerializer(serializers.ModelSerializer):
    """
    Base serializer for read-only endpoints.
    All fields are automatically set to read_only=True.
    """
    
    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


class BulkCreateSerializer(serializers.ListSerializer):
    """
    Serializer for bulk create operations.
    
    Usage:
        class MySerializer(serializers.ModelSerializer):
            class Meta:
                model = MyModel
                fields = '__all__'
                list_serializer_class = BulkCreateSerializer
    """
    
    def create(self, validated_data):
        instances = [self.child.Meta.model(**item) for item in validated_data]
        return self.child.Meta.model.objects.bulk_create(instances)


class ErrorSerializer(serializers.Serializer):
    """Serializer for error responses."""
    
    message = serializers.CharField()
    code = serializers.CharField(required=False)
    details = serializers.DictField(required=False)


class SuccessSerializer(serializers.Serializer):
    """Serializer for success responses."""
    
    message = serializers.CharField()
    data = serializers.DictField(required=False)


class PaginationSerializer(serializers.Serializer):
    """Serializer for pagination metadata."""
    
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file uploads."""
    
    file = serializers.FileField()
    description = serializers.CharField(required=False, allow_blank=True)
    
    def validate_file(self, value):
        """Validate file size and type."""
        # Max file size: 10MB
        max_size = 10 * 1024 * 1024
        
        if value.size > max_size:
            raise serializers.ValidationError('File size cannot exceed 10MB.')
        
        return value


class ImageUploadSerializer(serializers.Serializer):
    """Serializer for image uploads."""
    
    image = serializers.ImageField()
    alt_text = serializers.CharField(required=False, allow_blank=True)
    
    def validate_image(self, value):
        """Validate image size and format."""
        # Max image size: 5MB
        max_size = 5 * 1024 * 1024
        
        if value.size > max_size:
            raise serializers.ValidationError('Image size cannot exceed 5MB.')
        
        # Allowed formats
        allowed_formats = ['JPEG', 'JPG', 'PNG', 'GIF', 'WEBP']
        
        from PIL import Image
        try:
            img = Image.open(value)
            if img.format not in allowed_formats:
                raise serializers.ValidationError(
                    f'Image format must be one of: {", ".join(allowed_formats)}'
                )
        except Exception as e:
            raise serializers.ValidationError('Invalid image file.')
        
        return value


class DateRangeSerializer(serializers.Serializer):
    """Serializer for date range filtering."""
    
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    
    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError('start_date must be before end_date.')
        
        return attrs


class BulkDeleteSerializer(serializers.Serializer):
    """Serializer for bulk delete operations."""
    
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    
    def validate_ids(self, value):
        if len(value) > 100:
            raise serializers.ValidationError('Cannot delete more than 100 items at once.')
        return value

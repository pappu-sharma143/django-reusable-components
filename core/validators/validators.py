"""
Django Custom Validators

Comprehensive collection of reusable validators for models and forms.
"""

import re
import json
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime
from PIL import Image


# ============================================================================
# FIELD VALIDATORS
# ============================================================================

def validate_phone_number(value):
    """
    Validate international phone number format.
    Accepts formats: +1234567890, (123) 456-7890, 123-456-7890
    """
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')
    cleaned = re.sub(r'[\s\-\(\)]', '', value)
    
    if not phone_regex.match(cleaned):
        raise ValidationError(
            _('Enter a valid phone number. Format: +1234567890'),
            code='invalid_phone'
        )


def validate_email_domain(allowed_domains):
    """
    Validate email against allowed domains.
    
    Usage:
        validators=[validate_email_domain(['company.com', 'example.com'])]
    """
    def validator(value):
        domain = value.split('@')[-1].lower()
        if domain not in [d.lower() for d in allowed_domains]:
            raise ValidationError(
                _('Email domain must be one of: %(domains)s'),
                params={'domains': ', '.join(allowed_domains)},
                code='invalid_domain'
            )
    return validator


def validate_file_size(max_mb=10):
    """
    Validate file size limit.
    
    Usage:
        validators=[validate_file_size(max_mb=5)]
    """
    def validator(value):
        filesize = value.size
        max_size = max_mb * 1024 * 1024  # Convert MB to bytes
        
        if filesize > max_size:
            raise ValidationError(
                _('File size cannot exceed %(max_size)s MB. Current size: %(current_size)s MB'),
                params={
                    'max_size': max_mb,
                    'current_size': round(filesize / (1024 * 1024), 2)
                },
                code='file_too_large'
            )
    return validator


def validate_file_extension(allowed_extensions):
    """
    Validate file extension.
    
    Usage:
        validators=[validate_file_extension(['pdf', 'docx', 'txt'])]
    """
    def validator(value):
        ext = value.name.split('.')[-1].lower()
        if ext not in [e.lower() for e in allowed_extensions]:
            raise ValidationError(
                _('File extension must be one of: %(extensions)s'),
                params={'extensions': ', '.join(allowed_extensions)},
                code='invalid_extension'
            )
    return validator


def validate_image_dimensions(min_width=None, max_width=None, min_height=None, max_height=None):
    """
    Validate image dimensions.
    
    Usage:
        validators=[validate_image_dimensions(min_width=100, max_width=2000)]
    """
    def validator(value):
        try:
            img = Image.open(value)
            width, height = img.size
            
            if min_width and width < min_width:
                raise ValidationError(
                    _('Image width must be at least %(min_width)s pixels. Current: %(width)s'),
                    params={'min_width': min_width, 'width': width},
                    code='image_too_narrow'
                )
            
            if max_width and width > max_width:
                raise ValidationError(
                    _('Image width cannot exceed %(max_width)s pixels. Current: %(width)s'),
                    params={'max_width': max_width, 'width': width},
                    code='image_too_wide'
                )
            
            if min_height and height < min_height:
                raise ValidationError(
                    _('Image height must be at least %(min_height)s pixels. Current: %(height)s'),
                    params={'min_height': min_height, 'height': height},
                    code='image_too_short'
                )
            
            if max_height and height > max_height:
                raise ValidationError(
                    _('Image height cannot exceed %(max_height)s pixels. Current: %(height)s'),
                    params={'max_height': max_height, 'height': height},
                    code='image_too_tall'
                )
        except Exception as e:
            raise ValidationError(_('Invalid image file.'), code='invalid_image')
    
    return validator


def validate_alphanumeric(value):
    """Validate that value contains only letters and numbers."""
    if not value.isalnum():
        raise ValidationError(
            _('Only letters and numbers are allowed.'),
            code='not_alphanumeric'
        )


def validate_no_special_chars(value):
    """Validate that value contains no special characters."""
    if not re.match(r'^[a-zA-Z0-9\s]+$', value):
        raise ValidationError(
            _('Special characters are not allowed.'),
            code='contains_special_chars'
        )


def validate_positive_number(value):
    """Validate that value is a positive number."""
    if value <= 0:
        raise ValidationError(
            _('Value must be a positive number.'),
            code='not_positive'
        )


def validate_url_format(value):
    """Validate URL structure."""
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError(
            _('Enter a valid URL.'),
            code='invalid_url'
        )


def validate_date_not_past(value):
    """Validate that date is not in the past."""
    if isinstance(value, datetime):
        value = value.date()
    
    if value < date.today():
        raise ValidationError(
            _('Date cannot be in the past.'),
            code='date_in_past'
        )


def validate_date_not_future(value):
    """Validate that date is not in the future."""
    if isinstance(value, datetime):
        value = value.date()
    
    if value > date.today():
        raise ValidationError(
            _('Date cannot be in the future.'),
            code='date_in_future'
        )


def validate_age_range(min_age=0, max_age=150):
    """
    Validate age from birthdate.
    
    Usage:
        validators=[validate_age_range(min_age=18, max_age=100)]
    """
    def validator(value):
        if isinstance(value, datetime):
            value = value.date()
        
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < min_age:
            raise ValidationError(
                _('Age must be at least %(min_age)s years.'),
                params={'min_age': min_age},
                code='age_too_young'
            )
        
        if age > max_age:
            raise ValidationError(
                _('Age cannot exceed %(max_age)s years.'),
                params={'max_age': max_age},
                code='age_too_old'
            )
    
    return validator


def validate_credit_card(value):
    """Validate credit card number using Luhn algorithm."""
    # Remove spaces and hyphens
    number = re.sub(r'[\s\-]', '', value)
    
    if not number.isdigit():
        raise ValidationError(
            _('Credit card number must contain only digits.'),
            code='invalid_credit_card'
        )
    
    # Luhn algorithm
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    if luhn_checksum(number) != 0:
        raise ValidationError(
            _('Invalid credit card number.'),
            code='invalid_credit_card'
        )


def validate_postal_code(country='US'):
    """
    Validate postal/zip codes.
    
    Usage:
        validators=[validate_postal_code(country='US')]
    """
    patterns = {
        'US': r'^\d{5}(-\d{4})?$',
        'UK': r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$',
        'CA': r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$',
        'IN': r'^\d{6}$',
    }
    
    def validator(value):
        pattern = patterns.get(country)
        if not pattern:
            return  # Skip validation for unknown countries
        
        if not re.match(pattern, value.upper()):
            raise ValidationError(
                _('Invalid postal code for %(country)s.'),
                params={'country': country},
                code='invalid_postal_code'
            )
    
    return validator


def validate_username(value):
    """Validate username format (alphanumeric, underscore, hyphen, 3-30 chars)."""
    if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', value):
        raise ValidationError(
            _('Username must be 3-30 characters long and contain only letters, numbers, underscores, and hyphens.'),
            code='invalid_username'
        )


def validate_password_strength(min_length=8, require_uppercase=True, require_lowercase=True, 
                               require_digit=True, require_special=True):
    """
    Validate password complexity.
    
    Usage:
        validators=[validate_password_strength(min_length=10, require_special=False)]
    """
    def validator(value):
        if len(value) < min_length:
            raise ValidationError(
                _('Password must be at least %(min_length)s characters long.'),
                params={'min_length': min_length},
                code='password_too_short'
            )
        
        if require_uppercase and not re.search(r'[A-Z]', value):
            raise ValidationError(
                _('Password must contain at least one uppercase letter.'),
                code='password_no_uppercase'
            )
        
        if require_lowercase and not re.search(r'[a-z]', value):
            raise ValidationError(
                _('Password must contain at least one lowercase letter.'),
                code='password_no_lowercase'
            )
        
        if require_digit and not re.search(r'\d', value):
            raise ValidationError(
                _('Password must contain at least one digit.'),
                code='password_no_digit'
            )
        
        if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError(
                _('Password must contain at least one special character.'),
                code='password_no_special'
            )
    
    return validator


def validate_color_hex(value):
    """Validate hex color codes (#RRGGBB or #RGB)."""
    if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
        raise ValidationError(
            _('Enter a valid hex color code (e.g., #FF0000 or #F00).'),
            code='invalid_hex_color'
        )


def validate_ip_address(value):
    """Validate IPv4/IPv6 addresses."""
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    
    if not (re.match(ipv4_pattern, value) or re.match(ipv6_pattern, value)):
        raise ValidationError(
            _('Enter a valid IP address.'),
            code='invalid_ip'
        )


def validate_json_structure(schema):
    """
    Validate JSON against schema.
    
    Usage:
        validators=[validate_json_structure({'required': ['name', 'email']})]
    """
    def validator(value):
        try:
            data = json.loads(value) if isinstance(value, str) else value
            
            # Simple schema validation
            if 'required' in schema:
                for field in schema['required']:
                    if field not in data:
                        raise ValidationError(
                            _('Missing required field: %(field)s'),
                            params={'field': field},
                            code='missing_field'
                        )
        except json.JSONDecodeError:
            raise ValidationError(
                _('Invalid JSON format.'),
                code='invalid_json'
            )
    
    return validator


def validate_social_security(value):
    """Validate SSN format (US): XXX-XX-XXXX."""
    if not re.match(r'^\d{3}-\d{2}-\d{4}$', value):
        raise ValidationError(
            _('Enter a valid Social Security Number (XXX-XX-XXXX).'),
            code='invalid_ssn'
        )


# ============================================================================
# MODEL VALIDATORS
# ============================================================================

def validate_date_range(start_field, end_field):
    """
    Validate that start date is before end date.
    Use in model's clean() method.
    """
    def validator(instance):
        start = getattr(instance, start_field)
        end = getattr(instance, end_field)
        
        if start and end and start > end:
            raise ValidationError({
                end_field: _('End date must be after start date.')
            })
    
    return validator


def validate_price_range(min_price=0, max_price=None):
    """Validate price within range."""
    def validator(value):
        if value < min_price:
            raise ValidationError(
                _('Price must be at least %(min_price)s.'),
                params={'min_price': min_price},
                code='price_too_low'
            )
        
        if max_price and value > max_price:
            raise ValidationError(
                _('Price cannot exceed %(max_price)s.'),
                params={'max_price': max_price},
                code='price_too_high'
            )
    
    return validator


def validate_quantity_limits(min_qty=1, max_qty=None):
    """Validate quantity limits."""
    def validator(value):
        if value < min_qty:
            raise ValidationError(
                _('Quantity must be at least %(min_qty)s.'),
                params={'min_qty': min_qty},
                code='quantity_too_low'
            )
        
        if max_qty and value > max_qty:
            raise ValidationError(
                _('Quantity cannot exceed %(max_qty)s.'),
                params={'max_qty': max_qty},
                code='quantity_too_high'
            )
    
    return validator


def validate_discount_percentage(value):
    """Validate discount is between 0-100%."""
    if not (0 <= value <= 100):
        raise ValidationError(
            _('Discount percentage must be between 0 and 100.'),
            code='invalid_discount'
        )

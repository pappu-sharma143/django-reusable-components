# Django Validators

Comprehensive collection of custom validators for Django models and forms.

## Overview

This module provides reusable validators for common validation scenarios including phone numbers, emails, files, images, dates, and more.

## Usage

Import validators in your models or forms:

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

## Available Validators

### Field Validators

#### `validate_phone_number(value)`
Validates international phone number format.

#### `validate_email_domain(allowed_domains)`
Validates email against allowed domains.

```python
validators=[validate_email_domain(['company.com', 'example.com'])]
```

#### `validate_file_size(max_mb=10)`
Validates file size limit.

#### `validate_file_extension(allowed_extensions)`
Validates file extension.

```python
validators=[validate_file_extension(['pdf', 'docx', 'txt'])]
```

#### `validate_image_dimensions(min_width=None, max_width=None, min_height=None, max_height=None)`
Validates image dimensions.

#### `validate_alphanumeric(value)`
Ensures only letters and numbers.

#### `validate_no_special_chars(value)`
Ensures no special characters.

#### `validate_positive_number(value)`
Validates positive integers/floats.

#### `validate_url_format(value)`
Validates URL structure.

#### `validate_date_not_past(value)`
Ensures date is in the future.

#### `validate_date_not_future(value)`
Ensures date is in the past.

#### `validate_age_range(min_age=0, max_age=150)`
Validates age from birthdate.

#### `validate_credit_card(value)`
Validates credit card number using Luhn algorithm.

#### `validate_postal_code(country='US')`
Validates postal/zip codes.

#### `validate_username(value)`
Validates username format (alphanumeric, underscore, hyphen).

#### `validate_password_strength(min_length=8, require_uppercase=True, require_lowercase=True, require_digit=True, require_special=True)`
Validates password complexity.

#### `validate_color_hex(value)`
Validates hex color codes (#RRGGBB).

#### `validate_ip_address(value)`
Validates IPv4/IPv6 addresses.

#### `validate_json_structure(schema)`
Validates JSON against schema.

#### `validate_social_security(value)`
Validates SSN format (US).

### Model Validators

#### `validate_unique_together_case_insensitive(model, fields)`
Case-insensitive unique together validation.

#### `validate_date_range(start_field, end_field)`
Ensures start date is before end date.

#### `validate_price_range(min_price=0, max_price=None)`
Validates price within range.

#### `validate_quantity_limits(min_qty=1, max_qty=None)`
Validates quantity limits.

#### `validate_discount_percentage(value)`
Validates discount is between 0-100%.

## Examples

### Model Example

```python
from django.db import models
from core.validators import (
    validate_phone_number,
    validate_file_size,
    validate_image_dimensions,
    validate_password_strength
)

class User(models.Model):
    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )
    avatar = models.ImageField(
        validators=[
            validate_file_size(max_mb=2),
            validate_image_dimensions(min_width=100, min_height=100)
        ]
    )
```

### Form Example

```python
from django import forms
from core.validators import validate_email_domain, validate_alphanumeric

class RegistrationForm(forms.Form):
    email = forms.EmailField(
        validators=[validate_email_domain(['company.com'])]
    )
    username = forms.CharField(
        validators=[validate_alphanumeric]
    )
```

## Testing

```bash
python manage.py test core.tests.test_validators
```

## Contributing

Add new validators following the existing patterns and include comprehensive tests.

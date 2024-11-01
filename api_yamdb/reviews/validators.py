from django.utils import timezone

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Latin alphabet symbols, numbers and underscore'
)


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Please enter a valid year!'
        )

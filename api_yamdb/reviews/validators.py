from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_past_year(value) -> None:
    if value > timezone.now().year:
        raise ValidationError('Please enter a valid year!')

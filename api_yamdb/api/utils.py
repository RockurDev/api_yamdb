from django.conf import settings
from django.core.mail import send_mail

from users.models import User


def send_confirmation_email(user: User, confirmation_code: str) -> None:
    """Send email with confirmation code to user."""

    send_mail(
        'API_YAMDB. Confirmation code',
        f'Your confirmation code: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
